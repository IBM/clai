#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

''' imports '''
from typing import List
from datetime import datetime
from clai.server.command_message import Action, NOOP_COMMAND
from clai.tools.colorize_console import Colorize

import requests 
import json
import os

''' globals '''
_real_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
_path_to_config_file = _real_path + '/config.json'

_config = json.loads( open(_path_to_config_file).read() )

_github_access_token = _config["github_personal_access_token"]
_github_username = _config["github_username"]
_github_repo = _config["github_repo"]
_github_url = "https://api.github.com/repos/{}".format("/".join(_github_repo))

_path_to_log_file =_config["path_to_log_file"]

_rasa_port_number = _config["rasa_port_number"]
_rasa_service = 'http://localhost:{}/model/parse'.format(_rasa_port_number)

class Service:
    def __init__(self):
        self.state = {
            "ready_flag"      : False, 
            "threshold"       : 0.9,
            "current_intent"  : None,
            "current_branch"  : None,
            "commit_details"  : None,
            "has_done_add"    : False,
            "has_done_commit" : False
        }

        self.gh_session = requests.Session()
        self.gh_session.auth = (_github_username, _github_access_token)


    def __call__(self, *args, **kwargs):

        # Set user command
        command = args[0]
        confidence = 0.0

        try:

            response = requests.post(_rasa_service, json={'text': command}).json()
            confidence = response["intent"]["confidence"]

            if confidence > self.state["threshold"]:
                self.state["current_intent"] = response["intent"]["name"]

        except Exception as ex:
            print("Method failed with status " + str(ex))

        if self.state["current_intent"] == "commit":

            if not self.state["ready_flag"]:
                self.state["ready_flag"] = True
                temp_description = "Ready to {}. Press execute to continue.".format(self.state["current_intent"])

                return [ Action(
                            suggested_command="git status | tee {}".format(_path_to_log_file),
                            execute=True,
                            description=None,
                            confidence=1.0
                            ), Action(
                                suggested_command=NOOP_COMMAND,
                                execute=True,
                                description=Colorize().info().append(temp_description).to_console(),
                                confidence=1.0
                                ) ] 

        if command == "execute":

            now = datetime.now()
            commit_message = now.strftime("%d/%m/%Y %H:%M:%S")

            # this should really go into post-execute #
            stdout = open(_path_to_log_file).read().split("\n")
            commit_description = ""
            current_branch = None

            for line in stdout:

                if line.startswith("On branch"):
                    current_branch = line.split()[-1]

                if line.strip().startswith("modified:"):
                    commit_description += line.strip() + " + "

            if commit_description: self.state["commit_details"] = commit_description
            if current_branch: self.state["current_branch"] = current_branch

            commit_description = self.state["commit_details"]

            respond = Action(
                        suggested_command='git commit -m "{}" -m "{}";'.format(commit_message, commit_description),
                        execute=False,
                        description=None,
                        confidence=1.0
                    )

            if self.state["has_done_add"]:
                return respond

            else: 
                return [ Action(
                            suggested_command='git add -A',
                            execute=True,
                            description="Adding untracked files...",
                            confidence=1.0
                        ), respond]


        if self.state["current_intent"] == "push":
            return Action(
                    suggested_command='git push',
                    execute=False,
                    description=None,
                    confidence=confidence
                )

        if self.state["current_intent"] == "merge":
            merge_url = "{}/pulls".format(_github_url)

            source = None
            target = "master"

            for entity in response["entities"]:
                if entity["entity"] == "source": source = entity["value"]
                if entity["entity"] == "target": target = entity["value"]

            if not source: source = self.state["current_branch"]

            payload = { "title" : "Dummy PR from gitbot", 
                        "body"  : "Example from the `gitbot` screencast. This will not be merged.",
                        "head"  : source,
                        "base"  : target }

            ping_github = json.loads(self.gh_session.post(merge_url, json=payload).text)
            return Action(
                    suggested_command=NOOP_COMMAND,
                    execute=True,
                    description="Success. Created PR {}".format(ping_github["number"]),
                    confidence=confidence
                )

        if self.state["current_intent"] == "comment":

            idx = 0
            comment = None

            for entity in response["entities"]:
                if entity["entity"] == "id": idx = entity["value"]
                if entity["entity"] == "comment": comment = entity["value"]

            idx = command.split('<')[-1].split('>')[0]
            comment_url = "{}/issues/{}/comments".format(_github_url, idx)

            payload = { "body" : comment }

            ping_github = json.loads(self.gh_session.post(comment_url, json=payload).text)
            return Action(
                    suggested_command=NOOP_COMMAND,
                    execute=True,
                    description="Success",
                    confidence=confidence
                )


    def parse_command(self, command: str, stdout: str):

        if command.startswith( "git checkout" ):
            self.state["current_branch"] = None

        if command.startswith( "git add" ):
            self.state["has_done_add"] = True

        if command.startswith( "commit" ):
            self.state["has_done_add"] = False
            self.state["has_done_commit"] = True

