#!/usr/bin/env bash

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

git clone -q -b master --depth 5 https://github.ibm.com/AI-Engineering/rltk.git


echo "  >> Installing RLTK library"
echo "==============================================================="

cd "${FRAMEWORK_DIR}/rltk"
pip3 install -q --user .


echo "  >> Installing python dependencies"
echo "==============================================================="

pip3 install -r requirements.txt