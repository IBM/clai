#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# pylint: disable=protected-access,broad-except
from time import sleep

MAX_SIZE_STDOUT = 5000000

def wait_server_is_started():
    sleep(2)


def read(socket, command, chunk_readed=None):
    data = ''
    try:
        socket.output._sock.recv(1)
        command_readed = False
        while True:
            # note that os.read does not work
            # because it does not TLS-decrypt
            # but returns the low-level encrypted data
            # one must use "socket.recv" instead
            data_bytes = socket.output._sock.recv(4096)
            if not data_bytes:
                break

            chunk = data_bytes.decode('utf8', errors='ignore')
            print(f'------ chunk >{chunk}')
            if chunk.endswith(']# '):
                print('----- end found')
                if data:
                    break
            else:
                data += chunk

            if chunk_readed:
                chunk_readed(chunk)

            data = data[-MAX_SIZE_STDOUT:]

    except Exception as exception:
        print(f'error: {exception}')
    return data


def execute_cmd(container, command):
    socket = container.exec_run(cmd="bash -l", stdin=True, tty=True, privileged=True, socket=True)

    wait_server_is_started()

    command_to_exec = command + '\n'
    socket.output._sock.send(command_to_exec.encode())

    data = read(socket, command)

    sleep(1)
    socket.output._sock.send(b"exit\n")

    print(f'the output is: {data}')
    return str(data)
