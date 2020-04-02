#!/bin/bash
bash -x
###############################################################
# Licensed Materials - Property of IBM
# “Restricted Materials of IBM”
#  Copyright IBM Corp. 2019 ALL RIGHTS RESERVED
###############################################################

###############################################################
#
# Author: Eli M. Dow <emdow@us.ibm.com>
#
###############################################################

# Looks for an environment var named CLAI_DOCKER_IMAGE_NAME. If not
# defined, uses the default flag value 'claiplayground' for the docker image.
image_name=${CLAI_DOCKER_IMAGE_NAME-"claiplayground"}

# Looks for an environment var named CLAI_DOCKER_CONTAINER_NAME. If not
# defined, uses the default flag value 'CLAIBotPlayground' for the container.
image_name=${CLAI_DOCKER_CONTAINER_NAME-"CLAIBotPlayground"}

# Looks for an environment var named CLAI_DOCKER_OUTPUT. If not
# defined, uses the default flag value 'STDOUT' and Docker output will be
# sent to STDOUT
output_file=${CLAI_DOCKER_OUTPUT-"STDOUT"}

# Controls where CLAI would store internal states for persistence
DefaultBaseDir="${HOME}/.clai"
HostBaseDir="${CLAI_BASEDIR:-${DefaultBaseDir}}"
ContainerBaseDir="/root/.clai"

# docker-run settings that we will always want:
#   Run docker in privileged / unrestricted mode                (--privileged)
#   Allocate a psuedo-terminal in the docker container          (-t)
#   Run docker with 2GB of memory                               (-m 2GB)
#   Provide a handy human readable name for the container       (--name ${CLAI_DOCKER_CONTAINER_NAME})
runargs="--privileged                               \
         -t                                         \
         -m 2g                                      \
         --name ${CLAI_DOCKER_CONTAINER_NAME}"

if [ -n "$CLAI_DOCKER_JENKINSBUILD" ]; then
    # Additional docker-run settings we will want when running from
    # a Jenkins pipeline stage:
    #   Mount a host directory to the container directory           (-v ${HostBaseDir}:/root)
    #   Use pytest as the entrypoint                                (--entrypoint pytest)
    
    runargs="${runargs}                                 \
             -v ${HostBaseDir}:/root                    \
             --entrypoint pytest"
else
    # Additional docker-run settings we will normally want:
    #   Run docker in a detached daemon mode                        (-d)
    #   Forward the ports to the localhost so we can SSH            (-P)
    #   Mount a host directory to the container directory           (-v ${HostBaseDir}:${ContainerBaseDir})
    
    runargs="${runargs}                                 \
             -d                                         \
             -P                                         \
             -v ${HostBaseDir}:${ContainerBaseDir}"
fi

docker_run_command="docker run ${runargs} $CLAI_DOCKER_IMAGE_NAME"

if [ -n "$CLAI_DOCKER_OUTPUT" ]; then
    docker_run_command="${docker_run_command} > $CLAI_DOCKER_OUTPUT"
fi
    
exec ${docker_run_command}

if [ -e "$CLAI_DOCKER_JENKINSBUILD" ]; then
    echo 'User for ssh is root and the default pass Bashpass'
fi
