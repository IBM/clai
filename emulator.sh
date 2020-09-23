#!/bin/bash -e

python3 -m pip install -r requirements_emulator.txt --ignore-installed
pushd ./bin
export PYTHONPATH=./..:$PYTHONPATH && python3 emulator.py
popd
