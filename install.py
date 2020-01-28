#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# pylint: disable=no-name-in-module,import-error
import json
import os
import ssl
import sys
import argparse
import getpass

from distutils.dir_util import copy_tree
from distutils.dir_util import remove_tree
from distutils.file_util import copy_file

from clai.datasource.config_storage import ConfigStorage
from clai.datasource.stats_tracker import StatsTracker
from clai.server.agent_datasource import AgentDatasource
from clai.tools.anonymizer import Anonymizer
from clai.tools.colorize_console import Colorize
from clai.tools.console_helper import print_complete, print_error
from clai.tools.file_util import append_to_file, get_rc_file, is_windows, get_setup_file, get_rc_files

SUPPORTED_SHELLS = ['bash']
URL_BASH_PREEXEC = 'http://raw.githubusercontent.com/rcaloras/bash-preexec/master/bash-preexec.sh'
BASH_PREEXEC = 'bash-preexec.sh'


def valid_python_version():
    return sys.version_info[0] == 3 and sys.version_info[1] >= 6


def is_root_user(args):
    return os.geteuid() == 0 or args.demo_mode


def get_shell(args):
    if args.shell is None:
        return os.path.basename(os.getenv('SHELL', ''))

    return args.shell


def clai_installed(path):
    expand_path = os.path.expanduser(path)
    return os.path.isfile(expand_path)


def binary_installed(path):
    return os.path.exists(path)


def parse_args():
    default_user_destdir = os.path.join(
        os.path.expanduser('/opt/local/share'),
        'clai',
    )

    parser = argparse.ArgumentParser(description='Install CLAI for all users.')

    parser.add_argument(
        '--shell',
        help="if you like to install for different shell",
        dest='shell',
        action='store'
    )

    parser.add_argument(
        '--demo',
        help="if you like to jump installation restrictions",
        dest='demo_mode',
        action='store_true'
    )

    parser.add_argument(
        '--system',
        help="if you like install it for all users.",
        dest='system',
        action='store_true',
        default=False
    )

    parser.add_argument(
        '--unassisted',
        help="Don't ask to he user for questions or inputs in the install process",
        dest='unassisted',
        action='store_true',
        default=False
    )

    parser.add_argument(
        '--no-skills',
        help="Don't install the default skills",
        dest='no_skills',
        action='store_true',
        default=False
    )

    parser.add_argument(
        '-d', '--destdir', metavar='DIR', default=default_user_destdir,
        help='set destination to DIR',
    )

    args = parser.parse_args()

    if not valid_python_version():
        print_error('You need install python 3.6 or upper is required.')
        sys.exit(1)

    if not is_root_user(args):
        print_error('You need root privileges for complete the installation process.')
        sys.exit(1)

    if is_windows():
        print_error("CLAI is not supported on Windows.")
        sys.exit(1)

    shell = get_shell(args)
    if shell not in SUPPORTED_SHELLS:
        print_error('%s is not supported yet.' % shell)
        sys.exit(1)

    if args.system:
        if args.destdir != default_user_destdir:
            print_error(
                'Custom paths incompatible with --system option.')
            sys.exit(1)

    return args


def mkdir(path):
    print("creating directory: %s" % path)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def cp_tree(from_path, to_path):
    print("copying folder from %s to %s" % (from_path, to_path))
    copy_tree(from_path, to_path)


def copy(file, to_path):
    print("copying file from %s to %s" % (file, to_path))
    copy_file(file, to_path, update=1)


def download_file(file_url, filename):
    print("Download %s" % file_url)
    from urllib import request
    # pylint: disable=protected-access
    ssl._create_default_https_context = ssl._create_unverified_context
    request.urlretrieve(file_url, filename=filename)


def remove(path):
    print("cleaning %s" % path)
    remove_tree(path)


def install_plugins_dependencies(path, plugin):
    print(f'installing dependencies of plugin {plugin}')
    result = os.system(f'{path}/fileExist.sh {plugin}')

    return result == 0


def cli_executable(cli_path):
    os.system(f'chmod 777 {cli_path}/clai-run')
    os.system(f'chmod 777 {cli_path}/fswatchlog')
    os.system(f'chmod 777 {cli_path}/obtain-command-id')
    os.system(f'chmod 777 {cli_path}/post-execution')
    os.system(f'chmod 777 {cli_path}/process-command')
    os.system(f'chmod 777 {cli_path}/restore-history')


def read_users(bin_path):
    with open(bin_path + '/usersInstalled.json') as json_file:
        users = json.load(json_file)
        print(users)
        return users


def register_the_user(bin_path, system):
    users = read_users(bin_path)
    user_path = os.path.expanduser(get_rc_file(system))
    if user_path not in users:
        users.append(user_path)

    with open(bin_path + '/usersInstalled.json', 'w') as json_file:
        json.dump(users, json_file)


def create_rc_file_if_not_exist(system):
    rc_file_path = os.path.expanduser(get_rc_file(system))
    if not os.path.isfile(rc_file_path):
        open(rc_file_path, 'a').close()


def ask_to_user(text):
    print(Colorize()
          .info()
          .append(f"{text} ")
          .append("(y/n)")
          .to_console())

    while True:
        command_input = input()
        if command_input in ('y', 'yes'):
            return True

        if command_input in ('n', 'not'):
            return False

        print(Colorize()
              .info()
              .append('choose yes[y] or not[n]')
              .to_console())


def save_report_info(unassisted, agent_datasource, bin_path, demo_mode):
    enable_report = True

    if demo_mode:
        enable_report = False
    elif not unassisted:
        enable_report = ask_to_user("Do you like send information to CLAI server to improve it?")

    agent_datasource.mark_report_enable(enable_report)
    stats_tracker = StatsTracker(sync=True, anonymizer=Anonymizer(alternate_path=f'{bin_path}/anonymize.json'))
    stats_tracker.report_enable = enable_report
    stats_tracker.log_install(getpass.getuser())


def execute(args):
    unassisted = args.unassisted
    no_skills = args.no_skills
    demo_mode = args.demo_mode
    bin_path = os.path.join(args.destdir, 'bin')
    code_path = os.path.join(bin_path, 'clai')
    cli_path = os.path.join(bin_path, 'bin')
    temp_path = '~/tmp'
    mkdir(f"{temp_path}/")

    create_rc_file_if_not_exist(args.system)

    if clai_installed(get_setup_file()):
        print_error('CLAI is already in you system. You should execute uninstall first')
        sys.exit(1)

    if not binary_installed(bin_path):
        mkdir(bin_path)
        mkdir(code_path)

        cp_tree('./clai', code_path)
        cp_tree('./bin', cli_path)
        copy('./scripts/clai.sh', bin_path)
        copy('./scripts/saveFilesChanges.sh', bin_path)
        copy('./configPlugins.json', bin_path)
        copy('./usersInstalled.json', bin_path)
        copy('./anonymize.json', bin_path)
        copy('./scripts/fileExist.sh', bin_path)

        os.system(f'chmod 775 {bin_path}/saveFilesChanges.sh')
        os.system(f'chmod 775 {bin_path}/fileExist.sh')
        os.system(f'chmod -R 777 {code_path}/server/plugins')
        os.system(f'chmod 777 {bin_path}/clai.sh')
        os.system(f'chmod 666 {bin_path}/configPlugins.json')
        os.system(f'chmod 666 {bin_path}/anonymize.json')
        os.system(f'chmod -R 777 {bin_path}')
        cli_executable(cli_path)

        download_file(URL_BASH_PREEXEC, filename='%s/%s' % (temp_path, BASH_PREEXEC))
        copy('%s/%s' % (temp_path, BASH_PREEXEC), bin_path)

    register_the_user(bin_path, args.system)
    append_setup_to_file(get_setup_file(), bin_path)
    register_file(args.system)

    if not no_skills:
        agent_datasource = AgentDatasource(
            config_storage=ConfigStorage(alternate_path=f'{bin_path}/configPlugins.json'))
        plugins = agent_datasource.all_plugins()
        for plugin in plugins:
            if plugin.default:
                installed = install_plugins_dependencies(bin_path, plugin.pkg_name)
                if installed:
                    agent_datasource.mark_plugins_as_installed(plugin.name, None)

        save_report_info(unassisted, agent_datasource, bin_path, demo_mode)

    remove(f"{temp_path}/")

    os.system(f'chmod -R 777 /var/tmp')

    print_complete("CLAI has been installed correctly, you need restart your shell.")


def register_file(system):
    rc_files = get_rc_files(system)
    for file in rc_files:
        print(f"registering {file}")
        append_to_file(file, "# CLAI setup\n")

        append_to_file(file, 'if ! [ ${#preexec_functions[@]} -eq 0 ]; then\n')
        append_to_file(file, '  if ! [[ " ${preexec_functions[@]} " =~ " preexec_override_invoke " ]]; then\n')
        append_to_file(file, f"     source {get_setup_file()} \n")
        append_to_file(file, '  fi\n')
        append_to_file(file, 'else\n')
        append_to_file(file, f" source {get_setup_file()} \n")
        append_to_file(file, 'fi\n')

        append_to_file(file, "# End CLAI setup\n")


def append_setup_to_file(rc_path, bin_path):
    append_to_file(rc_path, "\n export CLAI_PATH=%s" % bin_path)
    append_to_file(rc_path, "\n export PYTHONPATH=%s" % bin_path)
    append_to_file(
        rc_path,
        "\n[[ -f %s/bash-preexec.sh ]] && source %s/bash-preexec.sh" % (bin_path, bin_path))
    append_to_file(
        rc_path,
        "\n[[ -f %s/clai.sh ]] && source %s/clai.sh" % (bin_path, bin_path))


sys.exit(execute(parse_args()))
