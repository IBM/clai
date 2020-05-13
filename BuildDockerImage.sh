#!/bin/bash

#################################################################
# Licensed Materials - Property of IBM
# “Restricted Materials of IBM”
#  Copyright IBM Corp. 2019 ALL RIGHTS RESERVED
#################################################################

# Looks for an environment var named DOCKER_BUILD_FLAGS. If not
# defined, uses the default flag value '--no-cache' for the docker build.
# Ex.: To enable docker caching, export DOCKER_BUILD_FLAGS="" (empty value)
#      To then disable docker caching again, unset DOCKER_BUILD_FLAGS
flags=${DOCKER_BUILD_FLAGS-"--no-cache"}

echo "==============================================================="
echo ""
echo " Phase 1: Building CLAI Container $flags"
echo ""
echo "==============================================================="
time docker build -f Dockerfile.CLAI -t claiplayground . $flags
if [ $? -ne 0 ]
then
        echo "Failed to build CLAI Playground Container. Aborting Build."
        exit -1
fi

