#!/usr/bin/env python3
#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

""" Exports man pages to txt files """

import os
from threading import Thread, Event

"""
The following command can do the same thing but cannot handle timouts

find ./linux -type f -exec $SHELL -c '
    for i in "$@" ; do
        man "$i" | col -bx > "$i".txt
    done
' {} +
"""

dirs = ['linux']

# Event object used to send signals from one thread to another
stop_event = Event()
 

def convert(path):
    cmd = f'man {path} | col -bx > ./{path}.txt'
    os.system(cmd)
    os.system(f'mv ./{path}.txt ./{path}')

def recursiveWalk(folder):
    for folder_name, sub_folders, filenames in os.walk(folder):
        if sub_folders:
            for subfolder in sub_folders:
                recursiveWalk(subfolder)

        for filename in filenames:
            print(f'Converting: {folder_name}/{filename}')
            try:
                # We create another Thread
                action_thread = Thread(target=convert(f'{folder_name}/{filename}'))
        
                action_thread.start()
                action_thread.join(timeout=5)
    
                stop_event.set()
            except Exception as e:
                print(f'Error converting: {folder_name}/{filename}',e)
           

if __name__ == '__main__':
    [recursiveWalk(directory) for directory in dirs]

