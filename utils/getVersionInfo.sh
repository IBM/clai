#!/usr/bin/env bash
#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

read versionFile fieldName
cat $versionFile | grep $fieldName | awk '{print $3}' | sed 's/\"//g'
exit 0