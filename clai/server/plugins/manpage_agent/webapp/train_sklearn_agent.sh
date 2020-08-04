#!/bin/env bash

DIR="data/"
MANPAGES_DIR="data/manpages"
MODEL_DIR="data/model"


# Remove data folder if exists already
if [[ -d "${DIR}" ]]; then rm -Rf ${DIR}; fi
mkdir "${DIR}"

echo "==============================================================="
echo ""
echo " Phase 1: Installing necessary tools"
echo ""
echo "==============================================================="
# Install Python3 dependencies
echo ">> Installing python dependencies"
python3 -m pip install -r train_requirements.txt

echo "==============================================================="
echo ""
echo " Phase 2: Recovering manpages from the operating system"
echo ""
echo "==============================================================="
# Remove manpages folder if exists already
if [[ -d "${MANPAGES_DIR}" ]]; then rm -Rf ${MANPAGES_DIR}; fi

echo " >> Making manpages directory"
mkdir "${MANPAGES_DIR}"

echo " >> Getting a list of commands"
# Get a list of commands and store in file
man -k . | awk '{print $1}' | sed 's/(.*//' > "${MANPAGES_DIR}/cmds.txt"

echo " >> Getting manual page data for each command"
# Read each command from the file and extract man page content
while read -r line
do

	man ${line} | col -b > "${MANPAGES_DIR}/${line}.txt"

done< "${MANPAGES_DIR}/cmds.txt"

echo "==============================================================="
echo ""
echo " Phase 3: Building Elastic search index for forum and manpages"
echo ""
echo "==============================================================="
# Remove model folder if exists already
if [[ -d "${MODEL_DIR}" ]]; then rm -Rf ${MODEL_DIR}; fi

echo " >> Making manpages directory"
mkdir "${MODEL_DIR}"

python3 train_sklearn_agent.py

echo " >> Removing manpage corpus directory"
rm -rf "${MANPAGES_DIR}"

echo "==============================================================="
echo "                      Training complete "
echo "==============================================================="