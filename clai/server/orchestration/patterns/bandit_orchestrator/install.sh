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

git clone -q -b develop --depth 5 https://github.ibm.com/AI-Engineering/python-component-framework.git
git clone -q -b master --depth 5 https://github.ibm.com/AI-Engineering/bandit-core.git


echo "  >> Installing components library"
echo "==============================================================="

cd "${FRAMEWORK_DIR}/python-component-framework"
pip install -q --user .
NEW_PYTHONPATH="${FRAMEWORK_DIR}/python-component-framework/pycomp"


echo "  >> Installing bandit library"
echo "==============================================================="

cd "${FRAMEWORK_DIR}/bandit-core"
pip install -q --user .
NEW_PYTHONPATH="${NEW_PYTHONPATH}:${FRAMEWORK_DIR}/bandit-core/bandits:${FRAMEWORK_DIR}/bandit-core/patterns"


case `grep -F "${NEW_PYTHONPATH}" ~/.bashrc >/dev/null; echo $?` in
  1)
    echo "\n\n export PYTHONPATH=\""${PYTHONPATH}":"${NEW_PYTHONPATH}"\"\n" >> ~/.bashrc
    ;;
esac

echo "  >> Installing python dependencies"
pip3 install -r requirements.txt