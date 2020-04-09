#!/usr/bin/env python3
#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os


def getAllFiles(directory):
    return os.popen(f'find ./{directory} -type f ').read().split('\n')

def buildFileSets(directory):
    path_set = []
    name_set = []

    for path in getAllFiles(directory):
        filename = path.split('/')[-1]
        # remove the extensions
        name = filename.split('.')[0]
        path_set.append(path)
        name_set.append(name)

    return set(name_set)
            
def compareDirs(a,b):
    print(a.intersection(b))

    



if __name__ == '__main__':
    sets = [ buildFileSets(directory) for directory in ['linux', 'z']]
    compareDirs(sets[0], sets[1])