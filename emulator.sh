#!/bin/bash -e

pushd ./bin
export PYTHONPATH=./..:$PYTHONPATH && python3 emulator.py
popd