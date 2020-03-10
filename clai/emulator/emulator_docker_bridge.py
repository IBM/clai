# pylint: disable=protected-access

import multiprocessing as mp
import os
import tarfile
import traceback
from typing import Optional

import docker
from pytest_docker_tools.utils import wait_for_callable

from pytest_docker_tools.wrappers import Container

from clai.emulator.docker_message import DockerMessage, DockerReply
from clai.emulator.emulator_docker_log_connector import EmulatorDockerLogConnector
from clai.tools.docker_utils import wait_server_is_started, read


class EmulatorDockerBridge:

    def __init__(self):
        self.manager = mp.Manager()
        self.queue = self.manager.Queue()
        self.queue_out = self.manager.Queue()
        self.pool = mp.Pool(1)
        self.consumer_messages = None

        self.emulator_docker_log_conector = EmulatorDockerLogConnector(
            mp.Pool(1),
            self.manager.Queue(),
            self.queue_out)

    def start(self):
        print(f"-Start docker bridge-")
        self.emulator_docker_log_conector.start()
        self.consumer_messages = self.pool.map_async(
            __consumer__,
            ((self.queue, self.emulator_docker_log_conector.log_queue, self.queue_out),))
        self.__internal_send__(DockerMessage(docker_command='start'))

    def stop_server(self):
        self.__internal_send__(DockerMessage(docker_command='request_stop'))
        self.consumer_messages.wait(timeout=3)

    def request_skills(self):
        self.__internal_send__(DockerMessage(docker_command='request_skills', message="clai skills"))

    def select_skill(self, skill_name):
        self.__internal_send__(DockerMessage(docker_command='select_skill', message=f'clai activate {skill_name}'))

    def unselect_skill(self, skill_name):
        self.__internal_send__(DockerMessage(docker_command='unselect_skill', message=f'clai deactivate {skill_name}'))

    def send_message(self, message: str):
        self.__internal_send__(DockerMessage(docker_command='send_message', message=message))

    def refresh_files(self):
        self.__internal_send__(DockerMessage(docker_command='refresh', message="clai reload"))

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
        # pylint: disable=bare-except
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
    # pylint: disable=bare-except
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

    print(f"container run {my_clai.status} {my_clai.name}")

    return my_clai


def copy_files(my_clai):
    old_path = os.getcwd()
    print(f'Building {old_path}')
    srcpath = os.path.join(get_base_path(),
                           'clai', 'server', 'plugins')
    os.chdir(srcpath)

    tar = tarfile.open('temp.tar', mode='w')
    try:
        tar.add('.', recursive=True)
    finally:
        tar.close()

    data = open('temp.tar', 'rb').read()

    destdir = os.path.join(
        os.path.expanduser('/opt/local/share'),
        'clai', 'bin', 'clai', 'server', 'plugins'
    )

    # pylint: disable=protected-access
    my_clai._container.put_archive(destdir, data)

    os.chdir(old_path)

    print("Done the refresh")


def __consumer__(args):
    queue, log_queue, queue_out = args
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
            log_queue.put(DockerMessage(docker_command='start_logger', message=my_clai.name))

        elif docker_message.docker_command == 'send_message' \
                or docker_message.docker_command == 'request_skills' \
                or docker_message.docker_command == 'unselect_skill' \
                or docker_message.docker_command == 'refresh' \
                or docker_message.docker_command == 'select_skill':
            if my_clai:
                print(f'socket {socket}')
                if not socket:
                    socket = my_clai.exec_run(cmd="bash -l", stdin=True, tty=True,
                                              privileged=True, socket=True)
                    wait_server_is_started()

                if docker_message.docker_command == 'refresh':
                    copy_files(my_clai)


                command_to_exec = docker_message.message + '\n'
                socket.output._sock.send(command_to_exec.encode())
                stdout = read(socket)

                reply = None
                if docker_message.docker_command == 'request_skills' \
                        or docker_message.docker_command == 'unselect_skill':
                    reply = DockerReply(docker_reply='skills', message=stdout)
                elif docker_message.docker_command == 'send_message':
                    socket.output._sock.send("clai last-info\n".encode())
                    info = read(socket)
                    reply = DockerReply(docker_reply='reply_message', message=stdout, info=info)

                if reply:
                    queue_out.put(reply)
        elif docker_message == 'request_stop':
            if my_clai:
                my_clai.kill()
                break

        queue.task_done()
    print("----STOP CONSUMING-----")
