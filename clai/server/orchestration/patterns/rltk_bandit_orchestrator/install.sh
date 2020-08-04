#!/bin/env bash

echo "==============================================================="
echo ""
echo " Phase 1: Installing necessary tools"
echo ""
echo "==============================================================="

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
FRAMEWORK_DIR="${DIR}/framework"

if [ -d "${FRAMEWORK_DIR}" ]; then
  rm -rf "${FRAMEWORK_DIR}"
fi

mkdir -p "${FRAMEWORK_DIR}"


echo "  >> Cloning framework libraries"
echo "==============================================================="

cd "${FRAMEWORK_DIR}"

# Download and install RLTK library into the rltk folder and uncomment the
# bottom two lines


echo "  >> Installing RLTK library"
echo "==============================================================="

# cd "${FRAMEWORK_DIR}/rltk"
# python3 -m pip install -q --user .


echo "  >> Installing python dependencies"
echo "==============================================================="

python3 -m pip install -r requirements.txt