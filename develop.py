#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import sys
import ssl
import json
import argparse


from install import download_file
from install import register_file
from install import register_the_user
from install import append_setup_to_file
from install import install_orchestration
from install import install_plugins_dependencies

from uninstall import execute as uninstall

from clai.tools.file_util import get_setup_file
from clai.tools.console_helper import print_complete
from clai.datasource.stats_tracker import StatsTracker
from clai.datasource.config_storage import ConfigStorage
from clai.server.agent_datasource import AgentDatasource

platform = sys.platform

actions = ['install', 'uninstall']

install_directory = '/home/dev/.bin/clai/bin'

URL_BASH_PREEXEC = 'http://raw.githubusercontent.com/rcaloras/bash-preexec/master/bash-preexec.sh'
BASH_PREEXEC = 'bash-preexec.sh'

 
def parse_args():
    parser = argparse.ArgumentParser(description='Setup Clai in a development enviorment to make live changes')

    parser.add_argument('action', action="store", type=str, help=f'action for script to preform one of: {" ".join(actions)}')

    parser.add_argument(
        '-p','--path',
        help='path to source directory',
        dest='path',
        action='store'
    )

    args = parser.parse_args()

    if args.action not in actions:
        print(f'Error: "{args.action}" is not a valid action')
        print(f'Valid actions: {", ".join(actions)}')
        sys.exit(1)
    
    return args

def createInstallDir():
    try:
        if not os.path.exists(install_directory):
            print(f'creating install directory: {install_directory}')
            os.makedirs(install_directory, exist_ok=True)
        else:
            print(f'Install directory already exists')
    except Exception as e:
        print(e)
        sys.exit(1)

def link(src, dest):
    try:
        if not os.path.exists(dest):
            os.symlink(
                src,
                dest
            )
    except Exception as e:
        print(e)
        sys.exit(1)

def install(repo_path:str):
    createInstallDir()
   
    required_scripts = os.listdir(os.path.join(repo_path, 'scripts'))
    required_dirs = ['bin', 'clai']
    required_files = [file for file in os.listdir(repo_path) if file.endswith('.json') ]
    
    print('Linking all needed files to install directory')
    
    try:
        for script in required_scripts:
            link(
                os.path.join(repo_path, f'scripts/{script}'), 
                os.path.join(install_directory, script)
            )
            os.system(f'chmod 775 {os.path.join(install_directory, script)}')

        for directory in required_dirs:
            link(
                os.path.join(repo_path, directory),
                os.path.join(install_directory, directory)
            )
            if directory == 'bin':
                os.system(f'chmod -R 777 {os.path.join(install_directory, directory)}')

        for file in required_files:
            link(
                os.path.join(repo_path, file),
                os.path.join(install_directory, file)
            )
            os.system(f'chmod 666 {os.path.join(install_directory, file)}')

    except Exception as e:
        print(e)
        sys.exit(1)
    
    download_file(URL_BASH_PREEXEC, filename='%s/%s' % (install_directory, BASH_PREEXEC))
    register_the_user(install_directory, False)
    append_setup_to_file(get_setup_file(), install_directory)
    register_file(False)

    install_orchestration(install_directory)

    agent_datasource = AgentDatasource(
        config_storage=ConfigStorage(alternate_path=f'{install_directory}/configPlugins.json'))
    plugins = agent_datasource.all_plugins()
    for plugin in plugins:
        if plugin.default:
            installed = install_plugins_dependencies(install_directory, plugin.pkg_name)
            if installed:
                agent_datasource.mark_plugins_as_installed(plugin.name, None)
    
    print_complete("CLAI has been installed correctly, you need restart your shell.")

def revert():
    print('Reverting file permissions to original state')
    scripts = [ file for file in os.listdir(install_directory) if file.endswith('.sh') ]
    json_files = [ file for file in os.listdir(install_directory) if file.endswith('.json') ]

    try:
        for script in scripts:
            os.system(f'chmod 644 {os.path.join(install_directory, script)}')

        # Reset bin directory
        os.system(f'chmod 755 {install_directory}/bin')
        for file in os.listdir(f'{install_directory}/bin'):
            if file in ['emulator.py', 'process-command']:
                os.system(f'chmod 755 {os.path.join(install_directory, f"bin/{file}")}')
            else:
                os.system(f'chmod 644 {os.path.join(install_directory, f"bin/{file}")}')
        
        for file in json_files:
            os.system(f'chmod 666 {os.path.join(install_directory, file)}')

    except Exception as e:
        print(e)
        sys.exit(1)

def main(args: list):
    action = args.action
    repo_path = args.path
    
    if action == 'install':
        install(repo_path)
    elif action == 'uninstall':
        # revert file permissions back to normal
        revert()
        uninstall(['--user'])

    return 0
 

if __name__ == "__main__":
    sys.exit(main(parse_args()))