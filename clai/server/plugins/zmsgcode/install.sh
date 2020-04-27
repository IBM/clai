#!/usr/bin/env bash

echo "==============================================================="
echo " Phase 1: Installing necessary dependencies"
echo "==============================================================="
# Install Python3 dependencies
if [[ "$1" = "--user" ]]; then
    pip3 install --user -r requirements.txt
else
    sudo pip3 install -r requirements.txt
fi

