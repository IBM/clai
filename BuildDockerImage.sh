#!/bin/bash

################################################################
# Licensed Materials - Property of IBM
# “Restricted Materials of IBM”
#  Copyright IBM Corp. 2019 ALL RIGHTS RESERVED
################################################################

# Looks for an environment var named DOCKER_BUILD_FLAGS. If not
# defined, uses the default flag value '--no-cache' for the docker build.
# Ex.: To enable docker caching, export DOCKER_BUILD_FLAGS="" (empty value)
#      To then disable docker caching again, unset DOCKER_BUILD_FLAGS
flags=${DOCKER_BUILD_FLAGS-"--no-cache"}

# Looks for an environment var named CLAI_DOCKER_IMAGE_NAME. If not
# defined, uses the default flag value 'claiplayground' for the docker image.
image_name=${CLAI_DOCKER_IMAGE_NAME-"claiplayground"}

# Looks for an environment var named CLAI_DOCKER_JENKINSBUILD. If it is
# defined, adds it to the docker build command params.
buildargs=""
if [ -n "$CLAI_DOCKER_JENKINSBUILD" ]; then
    buildargs="--build-arg jenkinsbuild=true"
fi

echo "==============================================================="
echo ""
echo " Phase 1: Building CLAI Container $flags"
echo ""
echo "==============================================================="
time docker build -f Dockerfile.CLAI -t $image_name $buildargs . $flags
if [ $? -ne 0 ]
then
        echo "Failed to build CLAI Playground Container. Aborting Build."
        exit -1
fi

