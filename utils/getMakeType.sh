#!/usr/bin/env bash
#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

read arg
makestr=$($arg -V 2> /dev/null)

if [ -n "$makestr" ]; then
    echo "Makefile.uss"
else
    echo "Makefile.gnu"
fi

exit 0