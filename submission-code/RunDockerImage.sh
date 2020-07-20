#!/bin/bash

if [ "$#" -gt 0 ]; then
    TAG_NAME=$1
else
    TAG_NAME=nlc2cmd-challenge
fi


docker run -it --name "NLC2CMD-Challenge" "${TAG_NAME}"