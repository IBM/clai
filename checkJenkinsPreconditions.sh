#! /bin/bash

# Licensed Materials - Property of IBM
#
# ????-??? Copyright IBM Corp. 2020 All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

#
# checkJenkinsPreconditions.sh
#     Make sure that we are happy with our build environment before Jenkins runs
#
# Authors
#     Dan FitzGerald (danfitz@us.ibm.com)
#
# Revision History
#     03/30/2020
#         * Initial creation
#

# Make sure that we have sshpass installed
isSshpassThere=$(command -v sshpass)
if [ -z $isSshpassThere ]; then
    echo "no bin or alias named 'sshpass'; unable to continue"
    exit 1
fi

# The following checks will ONLY occur if the __JENKINSCHECK_IS_CONTAINER
# environment variable was set at script invocation
if [ -n "$__JENKINSCHECK_IS_CONTAINER" ]; then
    
    # Make sure that "python3" is an alias for python
    isPython3There=$(command -v python3)
    if [ -z $isPython3There ]; then
        echo "no bin or alias named 'python3'; unable to continue"
        exit 1
    fi

    # Make sure we have pip installed
    #isPipThere=$(command -v pip)
    #if [ -z $isPipThere ]; then
    #    echo "pip is not installed; unable to continue"
    #    exit 1
    #fi
    
    # Make sure that we have pytest installed
    isPytestThere=$(python3 -m pip freeze | grep pytest | wc -l)
    if [ $isPytestThere -eq 0 ]; then
        python3 -m pip install pytest
        if [ $? -ne 0 ]; then
            echo "pytest can not be installed; unable to continue"
            exit 1
        fi
    fi
    
    # Make sure that we have pytest_docker_tools installed
    isPytestDockerToolsThere=$(python3 -m pip freeze | grep pytest_docker_tools | wc -l)
    if [ $isPytestDockerToolsThere -eq 0 ]; then
        python3 -m pip install pytest_docker_tools
        if [ $? -ne 0 ]; then
            echo "pytest_docker_tools can not be installed; unable to continue"
            exit 1
        fi
    fi
fi

# All's well
exit 0
