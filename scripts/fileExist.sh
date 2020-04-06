#!/bin/bash -e
flags=""
PLUGIN=$1

# Check for user passed args
while test $# != 0
do
    case "$1" in
      --user) 
        USER_INSTALL=true
        flags="$flags --user"
      ;;
       --path) 
        CLAI_PATH=$1
      ;;
      # add more flags here
      *) 
    esac
    shift
done


install_darwin () {
    code=1
    pushd $CLAI_PATH/clai/server/plugins/$PLUGIN
    if [ -f $CLAI_PATH/clai/server/plugins/$PLUGIN/install_darwin.sh ]; then
        eval "sh install_darwin.sh $flags"
        code=$?
    else
        if [ -f $CLAI_PATH/clai/server/plugins/$PLUGIN/install.sh ]; then
            eval "sh install.sh $flags"
            code=$?
        fi
    fi
    popd

    return $?
}

install_linux () {
    code=1
    cd $CLAI_PATH/clai/server/plugins/$PLUGIN
    eval "pwd"
    if [ -f $CLAI_PATH/clai/server/plugins/$PLUGIN/install_linux.sh ]; then
        eval "sh install_linux.sh $flags"
        code=$?
    else
        if [ -f $CLAI_PATH/clai/server/plugins/$PLUGIN/install.sh ]; then
            eval "sh install.sh $flags"
            code=$?
        fi
    fi

    return $code
}


install_plugin () {
    UNAME=$(uname -s)
    if [[ "$UNAME" == "Darwin"* ]]; then
        install_darwin $PLUGIN
    else
        install_linux $PLUGIN
    fi
    return $?
}

if [ -z "$CLAI_PATH" ]; then
    echo "Error: please pass the clai bin path using the --path flag"
    exit 1
fi

install_plugin $PLUGIN
if [ $? == 0 ]; then
        echo "Installed plugins dependencies  $CLAI_PATH/clai/server/plugins/$1/install.sh"
else
        echo "The plugin don't have dependencies $CLAI_PATH/clai/server/plugins/$1/install.sh"
fi