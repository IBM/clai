#!/bin/bash

################################################################
# Licensed Materials - Property of IBM
# “Restricted Materials of IBM”
# © Copyright IBM Corp. 2020 ALL RIGHTS RESERVED
################################################################

#
# runLocalTests.sh
#     Execute automated pytests for CLAI
#
# Authors
#     Dan FitzGerald <danfitz@us.ibm.com>
#
# Usage
#     runLocalTests.sh [OPTIONS]
#
#     Options:
#         -h
#               Display a usage message and exit
#
#         -n NAME
#               Perform a test named "test_NAME.py" or (if -p is specified)
#               "test_clai_plugins_NAME.py"
#
#         -p
#              Only perform tests on CLAI plugins
#
#         -v
#              Print verbose pytest output
#
# Notes:
#     If no options are specified, all pytest tests in the test directory will
#     be run.  If -p is specified but not -n, then all pydev tests for CLAI
#     plugins in the test directory will be run.
#
# Revision History
#     04/2020
#         * Initial creation
#

# Define constant variables
TEST_DIR="test"
if [ -z "$VIRTUAL_ENV" ]; then
    ROOT_DIR=""
else
    ROOT_DIR="$VIRTUAL_ENV"
fi
PYTHON_VERSION=`python3 -c 'import sys; print(str(sys.version_info[0])+"."+str(sys.version_info[1]))'`
PYTHONLIB="python${PYTHON_VERSION}/site-packages"

function displayUsage {
    echo ""
    echo "Usage: runLocalTests.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -n NAME"
    echo "     Perform a test named \"test_NAME.py\" or (if -p is specified) \"test_clai_plugins_NAME.py\""
    echo "  -p"
    echo "     Only perform tests on CLAI plugins"
    echo "  -v"
    echo "     Print verbose pytest output"
    echo ""
    echo "If no options are specified, all pytest tests in the test directory \
will be run.  If -p is specified but not -n, then all pydev tests for CLAI \
plugins in the test directory will be run."
    echo ""
}

# Parse command line arguments
while getopts ":hn:pv" opt; do
    case $opt in
        h )
            displayUsage
            exit 0
            ;;
            
        n )
            targets="$OPTARG"
            ;;
        
        p )
            onlyTestPlugins=true
            ;;
            
        v )
            verbose=true
            ;;
        
        \? )
            echo "Invalid Option: -$OPTARG" 1>&2
            exit 1
            ;;
        : )
            echo "Invalid Option: -$OPTARG requires an argument" 1>&2
            exit 1
            ;;
    esac
done

# Build our list of targeted test scripts
if [ -z "$targets" ] ; then
    if [ -n "$onlyTestPlugins" ] ; then
        targets=`ls $TEST_DIR/test_clai_plugins_*.py`
    else
        targets=`ls $TEST_DIR/test_*.py`
    fi
else
    if [ -n "$onlyTestPlugins" ] ; then
        targets=`ls $TEST_DIR/test_clai_plugins_${targets}.py`
    else
        targets=`ls $TEST_DIR/test_${targets}.py`
    fi
fi

echo "Preparing to run automated CLAI testing..."

# Configure our PYTHONPATH
if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH=.
fi
for dir in "${ROOT_DIR}" "${ROOT_DIR}/usr"; do
    for lib in lib lib64; do
        export PYTHONPATH="$PYTHONPATH:${dir}/${lib}/${PYTHONLIB}"
    done
done

# Make sure that we have pip installed
isPipThere=$(command -v pip3)
if [ -z $isPipThere ]; then
    echo "pip3 is not installed; unable to continue"
    exit 1
fi

# Make sure that pip is up to date
pip3 install --upgrade pip > /dev/null

# Install the prerequisites
for file in requirements.txt requirements_test.txt ; do
    pip3 install -r $file > /dev/null
    if [ $? -ne 0 ]; then
        echo "Prerequisites can not be installed; unable to continue"
        exit 1
    fi
done

numBucketsFailed=0
for target in $targets; do
    echo "Executing $target"
    
    pytestCommand='pytest-3'
    if [ -z "$verbose" ] ; then
        pytestCommand="${pytestCommand} -vra --tb=no"
    fi
    pytestCommand="${pytestCommand} ${target}"
    
    eval "${pytestCommand}"
    if [ $? -ne 0 ]; then
        let "numBucketsFailed=numBucketsFailed+1"
    fi
done
exit $numFailres
