#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

''' imports '''
from typing import List
from datetime import datetime
from clai.server.command_message import NOOP_COMMAND

import threading
import requests 
import json
import os

''' globals '''
_real_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
_path_to_config_file = _real_path + '/config.json'

_config = json.loads( open(_path_to_config_file).read() )

_github_access_token = _config["github_personal_access_token"]
_path_to_log_file =_config["path_to_log_file"]

_rasa_port_number = _config["rasa_port_number"]
_rasa_service = 'http://localhost:{}/model/parse'.format(_rasa_port_number)

class Service:
    def __init__(self):
        self.state = {
            "locked_flag"     : False, 
            "listening_flag"  : True,
            "threshold"       : 0.9,
            "current_intent"  : None,
            "current_branch"  : None,
            "commit_details"  : None,
            "has_done_add"    : False,
            "has_done_commit" : False
        }

    def __call__(self, *args, **kwargs):

        # Set user command
        command = args[0]
        confidence = 0.0

        if command == NOOP_COMMAND: self.state["locked_flag"] = False

        try:

            response = requests.post(_rasa_service, json={'text': command}).json()
            confidence = response["intent"]["confidence"]

            self.state["locked_flag"] = True

            if confidence > self.state["threshold"]:
                self.state["current_intent"] = response["intent"]["name"]

        except Exception as ex:
            print("Method failed with status " + str(ex))

        if self.state["current_intent"] == "commit" and self.state["locked_flag"]:

            now = datetime.now()
            commit_message = now.strftime("%d/%m/%Y %H:%M:%S")
            commit_description = self.state["commit_details"]

            command = 'git commit -m "{}" -m "{}";'.format(commit_message, commit_description)

            ####

            if self.state["has_done_add"]: 
                return [command]

                if self.state[commi]

            else: return ["git add -A", "git status | tee {}".format(_path_to_log_file), command]



        elif self.state["current_intent"] == "merge" and self.state["locked_flag"]:

            source = "origin"
            target = "master"

            if response["entities"]:

                for entity in response["entities"]:
                    if entity["entity"] == "source": source = entity["value"]
                    if entity["entity"] == "target": target = entity["value"]

            if not source: source = self.state["current_branch"]

            command = 'git push -u {} {}'.format(source, target)

            # open PR if one doesn't exist
            if not source: return ["git status | tee {}".format(_path_to_log_file), command]
            else: return [command]

        else: pass


    def parse_command(self, command: str, stdout: str):

        if command.startswith( "git checkout" ):
            self.state["current_branch"] = None

        if command.startswith( "git add" ):
            self.state["has_done_add"] = True

        if command.startswith( "commit" ):
            self.state["has_done_add"] = False
            self.state["has_done_add"] = True

        if self.state["listening_flag"]:

            if command.startswith( "git status" ):
                stdout = open(_path_to_log_file).read().split("\n")
                commit_description = ""
                current_branch = None

                for line in stdout:

                    if line.startswith("On branch"):
                        current_branch = line.split()[-1]

                    if line.strip().startswith("modified:"):
                        commit_description += line.strip() + "\n"

                if commit_description: self.state["commit_details"] = commit_description
                if current_branch: self.state["current_branch"] = current_branch

 