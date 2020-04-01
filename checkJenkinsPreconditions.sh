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

echo "This is a test"

# Make sure that "python3" is an alias for python
isPython3There=$(command -v python3)
if [ -z $isPython3There ]; then
    echo "no bin or alias named 'python3'; unable to continue"
    exit 1
fi

# Make sure that we have sshpass installed
isSshpassThere=$(command -v sshpass)
if [ -z $isSshpassThere ]; then
    echo "no bin or alias named 'sshpass'; unable to continue"
    exit 1
fi

# All's well
exit 0
