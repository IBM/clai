#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

#!/bin/env python

'''
This is a barebones implementation of what a closed-loop executor for a domain like IBM cloud might look like.
'''
from clai.server.command_message import Action, NOOP_COMMAND
import json, copy, os, re, threading

# import planner of choice
from clai.server.plugins.ibmcloud.planners import get_plan_from_pr2plan

'''
globals
'''
_real_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
_path_to_domain_file = _real_path + '/planning-files/domain.pddl'
_path_to_problem_template = _real_path + '/planning-files/template.pddl'
_path_to_yaml_temnplate = _real_path + '/sample-application-files/app.yaml'

'''
class :: track state of the user
'''
class KubeTracker():

    def __init__(self):

        self.domain = open(_path_to_domain_file, mode='r', encoding='utf-8-sig').read()
        self.template = open(_path_to_problem_template, mode='r', encoding='utf-8-sig').read()

        self.obs = []
        self.goal = None

        self.local_port = None
        self.host_port = None

        self.yaml = None
        self.namespace = None
        self.cluster_name = None
        self.protocol = None

        self.name = None
        self.tag = None

        # removal of images not implement yet
        self.image_to_remove = None

    def parse_command(self, command: str, stdout: str):

        if 'docker build' in command:

            temp = command.split(':')

            self.name = temp[0].split(' ')[-1]
            self.tag = temp[1].split(' ')[0]

            # restart logging observations if Dockerfile is built again
            self.refresh_observations()
            self.add_observation('(docker-build)')

        elif 'docker run' in command:
            self.add_observation('(docker-run)')

        elif 'ibmcloud ks clusters' in command:

            lines = stdout.split('\n')
            flag = False

            for line in lines:

                if flag:
                    self.cluster_name = line.strip().split(' ')[0].strip()
                    break

                if line.startswith('Name'):
                    flag = True

        elif 'ibmcloud account show' in command:
            if 'PAYG' not in stdout:
                self.protocol = 'NodePort'

        elif 'ibmcloud cr namespaces' in command:
            self.namespace = re.findall(r'Namespace\s+\n\w+', stdout)[0].strip().split('\n')[-1]

        else: pass

    def add_observation(self, obs: str):
        self.obs.append(obs)
        return self

    def get_observations(self) -> list:
        return self.obs

    def refresh_observations(self):
        # note :: non-empty --> this is a hack to get around empty observation error in pr2plan
        # note :: set-state actions sets initial state -- check domain.pddl for more information
        self.obs = ['set-state']
        return self

    def set_goal(self, utterance: str):
        # deploy to kube deploys local Dockerfile to your ibmcloud 
        # run Dockerfile brings up an application locally
        if utterance == 'deploy to kube':
            self.goal = '(deployed)'

        elif utterance == 'run Dockerfile':
            self.goal = '(docker_running)'

        elif utterance == 'build yaml':
            self.goal = '(known yaml)'

        # this is going to return an empty plan
        else: pass

        return self

'''
class :: execute actions from the planner
'''
class KubeExe(KubeTracker):

    def __init__(self):
        super().__init__()
        self.refresh_observations()

    def get_plan(self) -> list:
        problem = copy.deepcopy(self.template).replace('<GOAL>', self.goal)
        plan = get_plan_from_pr2plan(domain=self.domain, problem=problem, obs=self.get_observations())
        return plan

    def execute_action(self, action: str) -> str:
        try:

            command = getattr(self, action.replace('-', '_'))()
            if command: return command

        except Exception as e:
            print(e)

    def set_state(self):
        # set defaults
        if not self.host_port: self.host_port = '8085'
        if not self.name: self.name = 'app'
        if not self.tag: self.tag = 'v1'
        return None

    def docker_build(self):
        command = 'docker build -t {}:{} .'.format(self.name, self.tag)
        return Action(suggested_command=command, confidence=1.0, execute=False)

    def dockerfile_read(self):
        # read from Dockerfile
        with open('Dockerfile', 'r') as f:
            dockerfile_contents = f.read()

        self.local_port = re.findall(r'EXPOSE\s[0-9]+', dockerfile_contents)[0].strip().split(' ')[-1].strip()
        return None

    def docker_run(self):
        command = 'docker run -i -p {}:{} -d {}:{}'.format(self.host_port, self.local_port, self.name, self.tag)
        return Action(suggested_command=command, confidence=1.0)

    def ibmcloud_login(self):
        command = 'ibmcloud login'
        return Action(suggested_command=command, confidence=1.0)

    def ibmcloud_cr_login(self):
        command = 'ibmcloud cr login'
        return Action(suggested_command=command, confidence=1.0, execute=False)

    def get_namespace(self):
        command = 'ibmcloud cr namespaces'
        return None

    def docker_tag_for_ibmcloud(self):

        if not self.namespace: self.namespace = "<enter-namespace>"

        command = 'docker tag {}:{} us.icr.io/{}/{}:{}'.format(self.name, self.tag, self.namespace, self.name, self.tag)
        return Action(suggested_command=command, confidence=1.0, execute=False)

    def docker_push(self):

        if not self.namespace: self.namespace = "<enter-namespace>"

        command = 'docker push us.icr.io/{}/{}:{}'.format(self.namespace, self.name, self.tag)
        return Action(suggested_command=command, confidence=1.0, execute=False)

    def list_images(self):
        command = 'ibmcloud cr image-list'
        return Action(suggested_command=command, confidence=1.0, execute=False)

    def get_image_name_to_delete(self):
        return None

    def ibmcloud_delete_image(self):
        command = 'ibmcloud cr image-rm us.icr.io/{}/'.format(self.namespace, self.image_to_remove)
        return Action(suggested_command=command, confidence=1.0)

    def check_account_free(self):
        command = 'ibmcloud account show'
        return Action(suggested_command=command, confidence=1.0, execute=False)

    def check_account_paid(self):
        command = 'ibmcloud account show'
        return Action(suggested_command=command, confidence=1.0, execute=False)

    def set_protocol(self):
        return None

    def ask_protocol(self):
        description = 'Do you want to use NodePort protocol?'
        return Action(suggested_command=NOOP_COMMAND, description=description, confidence=1.0, execute=False)

    def build_yaml(self):
        # write to yaml file for deployment
        app_yaml = open(_path_to_yaml_temnplate, 'r').read()
        app_yaml = app_yaml.replace('{name}', self.name) \
            .replace('{tag}', self.tag) \
            .replace('{namespace}', self.namespace) \
            .replace('{protocol}', self.protocol) \
            .replace('{host_port}', self.host_port) \
            .replace('{local_port}', self.local_port)

        with open(_real_path + '/app.yaml', 'w') as f:
            f.write(app_yaml)

        self.yaml = app_yaml
        return Action(suggested_command=NOOP_COMMAND, description=self.yaml)

    def get_set_cluster_config(self):

        if not self.cluster_name: self.cluster_name = "<enter-cluster-name>"

        command = 'ibmcloud ks cluster-config {} | grep -e "export" | echo'.format(self.cluster_name)
        return Action(suggested_command=command, confidence=1.0)

    def kube_deploy(self):
        command = 'kubectl apply -f {}'.format(_path_to_yaml_temnplate)
        return Action(suggested_command=command, confidence=1.0)
