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

# Make sure that "python3" is an alias for python
isPython3There=$(command -v python3)
if [ -z $isPython3There ]; then
    echo "no bin or alias named 'python3'; unable to continue"
    exit 1
fi

# Make sure we have pip installed
isPipThere=$(command -v pip)
if [ -z $isPipThere ]; then
    echo "pip is not installed; unable to continue"
    exit 1
fi

# Make sure that we have pytest installed
isPytestThere=$(command -v pytest)
if [ -z $isPytestThere ]; then
    python3 -m pip install pytest
    if [ $? -ne 0 ]; then
        echo "pytest can not be installed; unable to continue"
        exit 1
    fi
fi

# Make sure that we have virtualenv installed
isVirtualenvThere=$(pip freeze | grep virtualenv | wc -l)
if [ $isVirtualenvThere -eq 0 ]; then
    python3 -m pip install virtualenv
    if [ $? -ne 0 ]; then
        echo "virtualenv can not be installed; unable to continue"
        exit 1
    fi
fi

# All's well
exit 0
