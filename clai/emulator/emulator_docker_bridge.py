import multiprocessing as mp
import os
import sys
import traceback
from typing import Optional

import docker
from pytest_docker_tools.utils import wait_for_callable

from pytest_docker_tools.wrappers import Container

from clai.emulator.docker_message import DockerMessage, DockerReply
from clai.tools.docker_utils import wait_server_is_started, read


class EmulatorDockerBridge:

    def __init__(self):
        self.manager = mp.Manager()
        self.queue = self.manager.Queue()
        self.queue_out = self.manager.Queue()
        self.pool = mp.Pool(1)
        self.consumer_messages = None

        self.my_clai: Optional[Container] = None

    def start(self):
        print(f"-Start docker bridge-")
        self.consumer_messages = self.pool.map_async(__consumer__, ((self.queue, self.queue_out),))
        self.__internal_send__(DockerMessage(docker_command='start'))

    def stop(self):
        self.__internal_send__(None)
        self.consumer_messages.wait(timeout=3)

    def send_message(self, message: str):
        self.__internal_send__(DockerMessage(docker_command='send_message', message=message))

    def __internal_send__(self, event: DockerMessage):
        try:
            print(f"sending to queue -> {event}")
            self.queue.put(event)
        # pylint: disable=broad-except
        except Exception as err:
            print(f"error sending: {err}")

    def retrieve_message(self) -> Optional[DockerReply]:
        try:
            message = self.queue_out.get(block=False)
            return message
        except:
            return None


def get_base_path():
    root_path = os.getcwd()
    if 'bin' in root_path:
        return '../'

    return '.'


def __get_image(docker_client):
    path = get_base_path()

    print(f'Building {path}')

    try:
        image, logs = docker_client.images.build(
            path=path,
            dockerfile='./clai/emulator/docker/centos/Dockerfile',
            rm=True
        )

        for log in logs:
            print(log)
    except:
        traceback.print_exc()

    return image


def __start_docker():
    docker_client = docker.from_env()

    image = __get_image(docker_client)

    docker_container = docker_client.containers.run(
        image=image.id,
        detach=True)

    my_clai = Container(docker_container)

    wait_for_callable('Waiting for container to be ready', my_clai.ready)

    print(f"container run {my_clai.status}")

    return my_clai


def __consumer__(args):
    print('¬¬')
    queue, queue_out = args
    my_clai = None
    socket = None
    print('starting reading from the queue')
    while True:
        docker_message: DockerMessage = queue.get()

        if docker_message is None:
            break

        print(f"message_received: {docker_message.docker_command}:{docker_message.message}")
        if docker_message.docker_command == 'start':
            my_clai = __start_docker()
        elif docker_message.docker_command == 'send_message':
            if my_clai:
                print(f'socket {socket}')
                if not socket:
                    socket = my_clai.exec_run(cmd="bash -l", stdin=True, tty=True,
                                              privileged=True, socket=True)
                    wait_server_is_started()

                command_to_exec = docker_message.message + '\n'
                socket.output._sock.send(command_to_exec.encode())
                stdout = read(socket, command_to_exec)

                reply = DockerReply(docker_reply='reply_message', message=stdout)
                queue_out.put(reply)

        queue.task_done()
    print("----STOP CONSUMING-----")
