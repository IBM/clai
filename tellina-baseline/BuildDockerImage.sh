#!/bin/bash

if [ "$#" -gt 0 ]; then
    TAG_NAME=$1
else
    TAG_NAME=nlc2cmd-challenge
fi

echo "Building nlc2cmd docker image"

# build docker image
docker build --force-rm -t ${TAG_NAME}  -f Dockerfile.nlc2cmd .

if [ $? -ne 0 ]
then
        echo "Failed to build nlc2cmd container. Aborting Build."
        exit -1
fi