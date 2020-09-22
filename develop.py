#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# pylint: disable=broad-except,invalid-name
import os
import sys
import json
import argparse

from install import download_file
from install import register_file
from install import clai_installed
from install import register_the_user
from install import append_setup_to_file
from install import install_orchestration
from install import install_plugins_dependencies

from uninstall import execute as uninstall

from clai.tools.file_util import get_setup_file
from clai.tools.console_helper import print_error
from clai.tools.console_helper import print_complete
from clai.datasource.config_storage import ConfigStorage
from clai.server.agent_datasource import AgentDatasource

from clai import PLATFORM

ACTIONS = ["install", "uninstall"]

DEFAULT_PORT = os.getenv('CLAI_PORT', '8010')

URL_BASH_PREEXEC = (
    "http://raw.githubusercontent.com/rcaloras/bash-preexec/master/bash-preexec.sh"
)
BASH_PREEXEC = "bash-preexec.sh"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Setup Clai in a development enviorment to make live changes"
    )

    parser.add_argument(
        "action",
        action="store",
        type=str,
        help=f'action for script to perform one of: {" ".join(ACTIONS)}',
    )

    parser.add_argument(
        "-p", "--path", help="path to source directory", dest="path", action="store"
    )

    parser.add_argument(
        "-i",
        "--install-directory",
        dest="install_path",
        action="store",
        type=str,
        help="The location that clai is installed in",
        default=f"{os.getenv('HOME', '/home/root')}/.bin/clai/bin"
    )

    args = parser.parse_args()

    if args.action not in ACTIONS:
        print_error(
            f"Not a valid action: '{args.action}' Valid actions: [{', '.join(ACTIONS)}]"
        )
        sys.exit(1)

    if args.path is None:
        print_error("The path flag is required")
        sys.exit(1)

    return args


def createInstallDir(directory):
    try:
        if not os.path.exists(directory):
            print(f"creating install directory: {directory}")
            os.makedirs(directory, exist_ok=True)
        else:
            print(f"Install directory already exists")
    except Exception as e:
        print(e)
        sys.exit(1)


def link(src, dest):
    try:
        if not os.path.exists(dest):
            os.symlink(src, dest)
    except Exception as e:
        print(e)
        sys.exit(1)


def install(repo_path: str, install_path: str):
    createInstallDir(install_path)

    required_scripts = os.listdir(os.path.join(repo_path, "scripts"))
    required_dirs = ["bin", "clai"]
    required_files = [file for file in os.listdir(repo_path) if file.endswith(".json")]

    print("Linking all needed files to install directory")

    try:
        for script in required_scripts:
            link(
                os.path.join(repo_path, f"scripts/{script}"),
                os.path.join(install_path, script),
            )
            os.system(f"chmod 775 {os.path.join(install_path, script)}")

        for directory in required_dirs:
            link(
                os.path.join(repo_path, directory),
                os.path.join(install_path, directory),
            )
            if directory == "bin":
                os.system(f"chmod -R 777 {os.path.join(install_path, directory)}")

        for file in required_files:
            link(os.path.join(repo_path, file), os.path.join(install_path, file))
            os.system(f"chmod 666 {os.path.join(install_path, file)}")

    except Exception as e:
        print(e)
        sys.exit(1)

    download_file(
        URL_BASH_PREEXEC, filename="%s/%s" % (install_path, BASH_PREEXEC)
    )

    register_the_user(install_path, False)
    append_setup_to_file(get_setup_file(), install_path, DEFAULT_PORT)
    register_file(False)

    install_orchestration(install_path)

    agent_datasource = AgentDatasource(
        config_storage=ConfigStorage(
            alternate_path=f"{install_path}/configPlugins.json"
        )
    )
    plugins = agent_datasource.all_plugins()
    for plugin in plugins:
        default = z_default = False
        if PLATFORM in ('zos', 'os390'):
            z_default = plugin.z_default
        else:
            default = plugin.default

        if default or z_default:
            installed = install_plugins_dependencies(install_path, plugin.pkg_name, False)
            if installed:
                agent_datasource.mark_plugins_as_installed(plugin.name, None)

    print_complete("CLAI has been installed correctly, you need restart your shell.")


def revert(install_path):
    print("Reverting file permissions to original state")
    scripts = [file for file in os.listdir(install_path) if file.endswith(".sh")]
    json_files = [
        file for file in os.listdir(install_path) if file.endswith(".json")
    ]

    try:
        for script in scripts:
            os.system(f"chmod 644 {os.path.join(install_path, script)}")

        # Reset bin directory
        os.system(f"chmod 755 {install_path}/bin")
        for file in os.listdir(f"{install_path}/bin"):
            if file in ["emulator.py", "process-command"]:
                os.system(f'chmod 755 {os.path.join(install_path, f"bin/{file}")}')
            else:
                os.system(f'chmod 644 {os.path.join(install_path, f"bin/{file}")}')

        for file in json_files:
            os.system(f"chmod 666 {os.path.join(install_path, file)}")

    except Exception as e:
        print(e)
        sys.exit(1)


def main(args: list):
    action = args.action
    repo_path = args.path
    install_path = args.install_path

    if action == "install":
        install(repo_path, install_path)
    elif action == "uninstall":
        path = clai_installed(get_setup_file())
        if not path:
            print_error("CLAI is not installed.")
            sys.exit(1)

        # revert file permissions back to normal
        revert(install_path)
        uninstall(["--user"])

        # revert plugins config
        with open(f"{repo_path}/configPlugins.json", "w") as file:
            file.write(
                json.dumps(
                    {
                        "selected": {"user": [""]},
                        "default": [""],
                        "default_orchestrator": "max_orchestrator",
                        "installed": [],
                        "report_enable": False,
                    }
                )
            )

    return 0


if __name__ == "__main__":
    sys.exit(main(parse_args()))
