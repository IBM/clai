#!/bin/bash -e

install_darwin () {
    code=1
    pushd /opt/local/share/clai/bin/clai/server/plugins/$1
    if [ -f /opt/local/share/clai/bin/clai/server/plugins/$1/install_darwin.sh ]; then
        eval "sh install_darwin.sh"
        code=$?
    else
        if [ -f /opt/local/share/clai/bin/clai/server/plugins/$1/install.sh ]; then
            eval "sh install.sh"
            code=$?
        fi
    fi
    popd

    return $?
}

install_linux () {
    code=1
    cd /opt/local/share/clai/bin/clai/server/plugins/$1
    eval "pwd"
    if [ -f /opt/local/share/clai/bin/clai/server/plugins/$1/install_linux.sh ]; then
        eval "sh install_linux.sh"
        code=$?
    else
        if [ -f /opt/local/share/clai/bin/clai/server/plugins/$1/install.sh ]; then
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

install_plugin $1
if [ $? == 0 ]; then
        echo "Installed plugins dependencies /opt/local/share/clai/bin/clai/server/plugins/$1/install.sh"
else
        echo "The plugin don't have dependencies /opt/local/share/clai/bin/clai/server/plugins/$1/install.sh"
fi