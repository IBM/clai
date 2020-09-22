import docker
from pytest_docker_tools.wrappers import Container

from clai.emulator.docker_message import DockerMessage, DockerReply
from clai.tools.docker_utils import wait_server_is_started, read


# pylint: disable=too-few-public-methods,protected-access
class EmulatorDockerLogConnector:
    def __init__(self, pool, log_queue, queue_out):
        self.pool_log = pool
        self.consumer_log = None
        self.log_queue = log_queue
        self.queue_out = queue_out

    def start(self):
        self.consumer_log = self.pool_log.map_async(__log_consumer__, ((self.log_queue, self.queue_out),))


def __log_consumer__(args):
    queue, queue_out = args
    my_clai: Container = None
    socket = None
    print('starting reading the log queue')
    while True:
        docker_message: DockerMessage = queue.get()
        if docker_message.docker_command == 'start_logger':
            docker_client = docker.from_env()
            docker_container = docker_client.containers.get(
                docker_message.message)
            my_clai = Container(docker_container)

        if my_clai:
            if not socket:
                socket = my_clai.exec_run(cmd="bash -l", stdin=True, tty=True,
                                          privileged=True, socket=True)
                wait_server_is_started()

            socket.output._sock.send('clai "none" tail -f /var/tmp/app.log\n'.encode())
            read(socket, lambda chunk: queue_out.put(DockerReply(docker_reply='log', message=chunk)))

        queue.task_done()
        queue.put(DockerMessage(docker_command='log'))
