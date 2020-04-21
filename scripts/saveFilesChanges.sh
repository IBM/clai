#!/bin/bash

eval '($CLAI_PATH/bin/fswatchlog "$1" "$2" >/dev/null &) > /dev/null'

exit 1