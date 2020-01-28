#!/bin/bash

if [ -f ../clai/server/plugins/$1/install.sh ]; then
        echo pwd
        pushd ../clai/server/plugins/$1
        eval "sh install.sh"
        popd
        echo "Installed plugins dependencies ../clai/server/plugins/$1/install.sh"
else
        echo "The plugin don't have dependencies ../clai/server/plugins/$1/install.sh"
fi
