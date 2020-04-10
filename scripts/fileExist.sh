#!/bin/bash -e
CLAI_PATH=$2

install_darwin () {
    code=1
    pushd $CLAI_PATH/clai/server/plugins/$1
    if [ -f $CLAI_PATH/clai/server/plugins/$1/install_darwin.sh ]; then
        eval "sh install_darwin.sh"
        code=$?
    else
        if [ -f $CLAI_PATH/clai/server/plugins/$1/install.sh ]; then
            eval "sh install.sh"
            code=$?
        fi
    fi
    popd

    return $?
}

install_linux () {
    code=1
    cd $CLAI_PATH/clai/server/plugins/$1
    eval "pwd"
    if [ -f $CLAI_PATH/clai/server/plugins/$1/install_linux.sh ]; then
        eval "sh install_linux.sh"
        code=$?
    else
        if [ -f $CLAI_PATH/clai/server/plugins/$1/install.sh ]; then
            eval "sh install.sh"
            code=$?
        fi
    fi

    return $code
}

install_plugin () {
    UNAME=$(uname -s)
    if [[ "$UNAME" == "Darwin"* ]]; then
        install_darwin $1
    else
        install_linux $1
    fi
    return $?
}

if [ -z "$2" ]; then
    echo "Error: please pass the clai bin path as the second argument"
    exit 1
fi

install_plugin $1
if [[ $? == 0 ]]; then
        echo "Installed plugins dependencies  $CLAI_PATH/clai/server/plugins/$1/install.sh"
else
        echo "The plugin don't have dependencies $CLAI_PATH/clai/server/plugins/$1/install.sh"
fi
