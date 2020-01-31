#!/usr/bin/env python
from typing import Dict, List, Tuple
import json, random
import numpy as np

'''
globals
'''
path_to_config_file = 'config.json'
saved_user_profiles = {"generic",
                       "ignore_clai",
                       "ignore_nlc2cmd",
                       "prioritize_manpages_over_forum"}

prob_low = 0.2
prob_high = 0.8

'''
class :: skill instantiated from config 
'''
class Skill():

    def __init__(self, config:Dict):
        self.name = config["name"]
        self.get_next_action_list = config["pre_process"]
        self.post_process_list = config["post_process"]

    def get_name(self) -> str:
        return self.name

    def return_get_next_action_list(self) -> List:
        return self.get_next_action_list

    def return_post_process_list(self) -> List:
        return self.post_process_list

    def respond(self, command:str) -> List:

        if not self.return_get_next_action_list():
            return self, None, 0.0

        for example in self.return_get_next_action_list():
            if command == example[0]:
                return self, example[1], np.random.normal(prob_high, 0.3)

        return self, random.choice(self.return_get_next_action_list())[1], np.random.normal(prob_low, 0.3)

'''
class :: simulate one turn on the command line 
'''
class Simulation():

    def __init__(self, user_profile: str):

        self.profile  = user_profile
        self.skills   = set()
        self.commands = set()

        # build skill set
        self.config = json.loads( open(path_to_config_file).read() )
        for skill in self.config["skills"]:
            new_skill = Skill(skill)
            self.skills.add(new_skill)

        # build overall set of commands
        for skill in self.skills: 

            for command in skill.return_get_next_action_list():
                self.commands.add( command[0] )

            for command in skill.return_post_process_list():
                self.commands.add( command[0] )

        # make a dummy skill corresponding to none selection        
        dummy_skill_defn = {"name" : "None", "pre_process" : [], "post_process" : []}

        for command in self.config["generic"]:
            dummy_skill_defn["pre_process"].append( [command, "None"] )
            self.commands.add( command )

        self.skills.add(Skill(dummy_skill_defn))

    def simulate(self, select_skill_name:str = None) -> Dict:

        new_command, user_response = self.generate_next_command()
        active_skills, selected_skill, suggested_command = self.clai_activity(new_command, select_skill_name)
        next_command, user_response = self.generate_next_command(prev_command = new_command, suggested_command = suggested_command)
        reward = self.compute_reward(new_command, active_skills, selected_skill, suggested_command, next_command, user_response)

        return { "prev_command"      : new_command,
                 "state_info"        : None,
                 "active_skills"     : active_skills,
                 "selected_skill"    : selected_skill,
                 "suggested_command" : suggested_command,
                 "user_response"     : user_response,
                 "reward"            : reward,
                 "next_command"      : next_command }


    def clai_activity(self, new_command:str, select_skill_name:str = None) -> List:

        active_skills = [skill.respond(new_command) for skill in self.skills]
        selected_skill = None
        suggested_command = None

        if select_skill_name:

            # select provided choice of skills
            for item in active_skills:
                if item[0].get_name() == select_skill_name:
                    return active_skills, item[0], item[0].respond(new_command)[1]
        else:

            # select using max confidence
            max_confidence = 0.0

            for item in active_skills:
                if item[2] > max_confidence:
                    selected_skill, suggested_command, max_confidence = item

            return active_skills, selected_skill, suggested_command


    def generate_next_command(self, prev_command:str = None, suggested_command:str = None) -> List[str]:

        user_response = ""
        command = None

        if suggested_command:

            for skill in self.skills:            
                if [prev_command, suggested_command] in skill.return_get_next_action_list():
                    # do the suggested action if part of the ground truth
                    return suggested_command, "y"

            return random.choice( list(self.commands) ), "n"
 
        # do a random action
        return random.choice( list(self.commands) ), "y"


    def compute_reward(self, new_command:str, active_skills:List[Skill], selected_skill:Skill, suggested_command:str, next_command:str, user_response:str) -> float:
        return eval( "self.__{}__(new_command, active_skills, selected_skill, suggested_command, next_command, user_response)".format(self.profile) )


    # this is the generic reward function
    # explicit signal :: user says yay or nay
    # implicit signal :: compute match between previous command and next command 
    def __generic__(self, new_command, active_skills, selected_skill, suggested_command, next_command, user_response) -> float:

        if suggested_command:

            if user_response == "y":
                return 1.0
            
            if user_response == "n":
                return 0.0

            return float(len( set( suggested_command.split() ).intersection( set( next_command.split() )))) / len( set( suggested_command.split() )) 

        return 0.0

    # this user persona hates the nlc2cmd skill
    def __ignore_nlc2cmd__(self, new_command, active_skills, selected_skill, suggested_command, next_command, user_response) -> float:

        if selected_skill:
            if selected_skill.get_name() == "nlc2cmd":
                return 0.0

        return self.__generic__(new_command, active_skills, selected_skill, suggested_command, next_command, user_response)

    # this user on MacOS prefers manpages since forums return answers more relevant to Unix systems
    def __prioritize_manpages_over_forum__(self, new_command, active_skills, selected_skill, suggested_command, next_command, user_response) -> float:

        if selected_skill:
            if selected_skill.get_name() == "man page explorer":

                if [new_command, suggested_command] in selected_skill.return_get_next_action_list():
                    return 1.0

                for item in active_skills:
                    # swap high confidence on howdoi with man page explorer
                    if item[0].get_name() == "howdoi" and item[2] > 0.7:
                        return 1.0

        return self.__generic__(new_command, active_skills, selected_skill, suggested_command, next_command, user_response)

    # this user wants to ignore CLAI altogether
    def __ignore_clai__(self, new_command, active_skills, selected_skill, suggested_command, next_command, user_response) -> float:

        if selected_skill:
            if selected_skill.get_name() == "None":
                return 1.0

        return 0.0


def main():
    new_simulation = Simulation(user_profile = "generic")

    for i in range(10):
        result = new_simulation.simulate()

        if result["selected_skill"]:
            print( i, result, result["selected_skill"].get_name() )
        else:
            print( i, result, None )

if __name__ == "__main__":
    main()


