#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import List

from clai.server.command_message import Action
from clai.server.command_runner.agent_descriptor import AgentDescriptor
from clai.server.orchestration.orchestrator_descriptor import OrchestratorDescriptor
from clai.tools.colorize_console import Colorize
from clai.tools.process_utils import check_if_process_running


def get_printable_name(plugin: AgentDescriptor):
    full_name = f"{plugin.name}"
    if plugin.installed:
        full_name = f"{full_name} (Installed)"
        if not plugin.ready:
            full_name = f"{full_name} (Starting)"
    else:
        full_name = f"{full_name} (Not Installed)"

    return full_name


def create_error_install(name: str) -> Action:
    text = (
        Colorize()
        .warning()
        .append(
            f"{name} is not a valid skill to add to the catalog. You need to write a folder or a valid url. \n"
        )
        .append("Example: clai install ./my_new_agent")
        .to_console()
    )

    return Action(suggested_command=":", description=text, execute=True)


def create_error_select(selected_plugin: str) -> Action:
    text = (
        Colorize()
        .warning()
        .append(f"'{selected_plugin}' is not a valid skill name. ")
        .append("To check available skills, issue:\n >> clai skills\n")
        .append("Example:\n >> clai activate nlc2cmd")
        .to_console()
    )

    return Action(suggested_command=":", description=text, execute=True)


def create_orchestrator_list(
    selected_orchestrator: str,
    all_orchestrator: List[OrchestratorDescriptor],
    verbose_mode=False,
) -> Action:
    text = "Available Orchestrators:\n"

    for orchestrator in all_orchestrator:
        if selected_orchestrator == orchestrator.name:
            text += (
                Colorize()
                .emoji(Colorize.EMOJI_CHECK)
                .complete()
                .append(f" {orchestrator.name}\n")
                .to_console()
            )

            if verbose_mode:
                text += (
                    Colorize()
                    .complete()
                    .append(f" {orchestrator.description}\n")
                    .to_console()
                )

        else:
            text += (
                Colorize()
                .emoji(Colorize.EMOJI_BOX)
                .append(f" {orchestrator.name}\n")
                .to_console()
            )

            if verbose_mode:
                text += Colorize().append(f" {orchestrator.description}\n").to_console()

    return Action(suggested_command=":", description=text, execute=True)


def create_message_list(
    selected_plugin: List[str], all_plugins: List[AgentDescriptor], verbose_mode=False
) -> Action:
    text = "Available Skills:\n"

    for plugin in all_plugins:
        if plugin.pkg_name in selected_plugin:
            text += (
                Colorize()
                .emoji(Colorize.EMOJI_CHECK)
                .complete()
                .append(f" {get_printable_name(plugin)}\n")
                .to_console()
            )

            if verbose_mode:
                text += (
                    Colorize().complete().append(f"{plugin.description}\n").to_console()
                )

        else:
            text += (
                Colorize()
                .emoji(Colorize.EMOJI_BOX)
                .append(f" {get_printable_name(plugin)}\n")
                .to_console()
            )

            if verbose_mode:
                text += Colorize().append(f"{plugin.description}\n").to_console()

    return Action(suggested_command=":", description=text, execute=True)


def create_message_server_runing() -> str:
    colorize = Colorize()
    if check_if_process_running():
        colorize.complete().append(f"The server is running")
    else:
        colorize.warning().append(f"The server is not running")

    return colorize.to_console()


def create_message_help() -> Action:
    text = (
        Colorize()
        .info()
        .append(
            "CLAI usage:\n"
            "clai [help] [skills [-v]] [orchestrate [name]] [activate [skill_name]] [deactivate [skill_name]] "
            "[manual | automatic] [install [name | url]] \n\n"
            "help           Print help and usage of clai.\n"
            "skills         List available skills. Use -v For a verbose description of each skill.\n"
            "orchestrate    Activate the orchestrator by name. If name is empty, list available orchestrators.\n"
            "activate       Activate the named skill.\n"
            "deactivate     Deactivate the named skill.\n"
            "manual         Disables automatic execution of commands without operator confirmation.\n"
            "auto           Enables automatic execution of commands without operator confirmation.\n"
            "install        Installs a new skill. The required argument may be a local file path\n"
            "               to a skill plugin folder, or it may be a URL to install a skill plugin \n"
            "               over a network connection.\n"
        )
        .to_console()
    )

    return Action(suggested_command=":", description=text, execute=True)
