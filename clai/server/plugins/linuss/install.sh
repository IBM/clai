#!/bin/env bash


echo "==============================================================="
echo ""
echo " Phase 1: Installing necessary tools"
echo ""
echo "==============================================================="
# Install Python3 dependencies
echo ">> Installing python dependencies"
if [[ "$1" = "--user" ]]; then
    pip3 install --user -r requirements.txt 2> /dev/null
else
    sudo pip3 install -r requirements.txt 2> /dev/null
fi

