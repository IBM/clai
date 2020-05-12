#!/bin/bash

################################################################
# Licensed Materials - Property of IBM
# Restricted Materials of IBM
# (C) Copyright IBM Corp. 2020 ALL RIGHTS RESERVED
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
#         -f
#               Ignore any "@unittest.skip()" statements in testcases;
#               does not affect any "@unittest.skipIf()" statements
#
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
    PIP_FLAGS="--user"
else
    ROOT_DIR="$VIRTUAL_ENV"
    PIP_FLAGS=""
fi
PYTHON_VERSION=`python3 -c 'import sys; print(str(sys.version_info[0])+"."+str(sys.version_info[1]))'`
PYTHONLIB="python${PYTHON_VERSION}/site-packages"
OPSYS=`uname -s`
if [ "$OPSYS" == "OS/390" ]; then
    PYTEST='pytest'
else
    PYTEST='python3 -m pytest'
fi
PIP3='python3 -m pip'

function displayUsage {
    echo ""
    echo "Usage: runLocalTests.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -f"
    echo "     Ignore any \"@unittest.skip()\" statements in testcases;"
    echo "     does not affect any \"@unittest.skipIf()\" statements."
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
while getopts ":fhn:pv" opt; do
    case $opt in
        f )
            force=true
            ;;
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

# If we're not already running on a system where CLAI is installed,
# we will want to install the CLAI dependencies
if [ "$OPSYS" != "OS/390" ]; then

    # Make sure that we have pip installed
    isPipThere=$(command -v pip3)
    if [ -z $isPipThere ]; then
        echo "pip is not installed; unable to continue"
        exit 1
    fi
    
    # Make sure that pip is up to date
    $PIP3 install $PIP_FLAGS --upgrade pip > /dev/null
    
    # Install the prerequisites
    for file in requirements.txt requirements_test.txt ; do
        $PIP3 install $PIP_FLAGS -r $file > /dev/null
        if [ $? -ne 0 ]; then
            echo "Prerequisites can not be installed; unable to continue"
            exit 1
        fi
    done
fi

if [ -n "$force" ] ; then
    if [ -d ".claitest" ]; then
        rm -rf .claitest/*
    else
        mkdir .claitest
    fi
fi

numBucketsFailed=0
for target in $targets; do
    echo "Executing $target"
    
    if [ -n "$force" ] ; then
        oldPrefix="$TEST_DIR/"
        newPrefix=".claitest/"
        newfile="${target/$oldPrefix/$newPrefix}"
        cp $target $newfile
        sed -i 's/@unittest.skip(/#@unittest.skip(/g' "$newfile"
        target="$newfile"
    fi
    
    pytestCommand='${PYTEST}'
    if [ -z "$verbose" ] ; then
        pytestCommand="${pytestCommand} -vra --tb=no"
    fi
    pytestCommand="${pytestCommand} ${target}"
    
    eval "${pytestCommand}"
    if [ $? -ne 0 ]; then
        let "numBucketsFailed=numBucketsFailed+1"
    fi
done

if [ -d ".claitest" ]; then
    rm -rf .claitest/*
    rmdir .claitest
fi

exit $numFailres
