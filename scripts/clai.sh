#!/bin/bash
function cleanUp() {
rm -f $ERROR_LOG_FILE;
}

function clear_history() {
    unset IFS
    eval "history -a";
    if [[ -f $CLAI_PATH/bin/restore-history ]]; then
      eval "$CLAI_PATH/bin/restore-history '${1}'";
    fi
    eval "history -n";
    eval "history -r"
}

preexec_override_invoke() {
    if [[ ! -f $CLAI_PATH/bin/post-execution ]]; then
      return 0;
    fi

    eval "set -o functrace > /dev/null 2>&1"
    eval "shopt -s extdebug > /dev/null 2>&1"
    # disable de command
    shopt -s extdebug

    export HISTFILE;
    eval "history -n";
    original_command=$(echo "$1")
    eval "set -o history -o histexpand";
    eval "history -a";
    IFS="|"
    args_pipe=
    num_commands=$(grep -c "|" <<< "$1")
    current_command_index=0
    for command in $(echo "$1")
    do
        command_id=$(eval "$CLAI_PATH/bin/obtain-command-id");
        USER_NAME=$(whoami)

        pending_commands_executed=0
        while [ $pending_commands_executed == 0 ]
        do
            eval "$CLAI_PATH/bin/process-command $command_id $USER_NAME '$command'";
            pending_commands_executed=$?
            eval "history -n";
            LAST_COMMAND=$(eval 'cat $HISTFILE | tail -n 1')
            CURRENT_PWD=$(eval 'pwd')

            sys_name=`uname -s`
            if [ "$sys_name" == "OS/390" ]
            then
                random_str=`date +%Y%m%d%H%M%S`
                if [[ ! "$TMPDIR" ]]
                then
                    ERROR_LOG_FILE="/tmp/tmp.$random_str"
                else
                    ERROR_LOG_FILE="$TMPDIR/tmp.$random_str"
                fi
                touch $ERROR_LOG_FILE
            else
                ERROR_LOG_FILE=$(mktemp);
            fi

            trap cleanUp EXIT
            if [ "$current_command_index" -lt "$num_commands" ]
            then
                if [ -z "$args_pipe" ]
                then
                    args_pipe=$(eval "$LAST_COMMAND" 2>$ERROR_LOG_FILE)
                else
                    args_pipe=$(eval "$LAST_COMMAND"<<< $args_pipe 2>$ERROR_LOG_FILE)
                fi
            else
                if [ -z "$args_pipe" ]
                then
                    eval "$LAST_COMMAND" 2>$ERROR_LOG_FILE
                else
                    eval "$LAST_COMMAND" <<< $args_pipe 2>$ERROR_LOG_FILE
                fi
            fi
            code=$?

        done
        if [[ -f $CLAI_PATH/bin/post-execution ]]; then
          eval "$CLAI_PATH/bin/post-execution $command_id $USER_NAME $code '${ERROR_LOG_FILE}'";
          cleanUp
        fi
	      ((current_command_index++))
        if [ $code != 0 ] ; then
           clear_history "${original_command}"
           return 4;
        fi
    done
    clear_history "${original_command}"
    return 4;
}

#subscribe the function
preexec_functions+=(preexec_override_invoke)

#launch server
if ! ps -Ao args | grep "[c]lai-run" > /dev/null 2>&1; then
  eval nohup $CLAI_PATH/bin/clai-run new &
fi

NEXT_WAIT_TIME=0
until ps -Ao args | grep "[c]lai-run" > /dev/null 2>&1 || [ $NEXT_WAIT_TIME -eq 3 ]; do
   sleep $(( NEXT_WAIT_TIME++ ))
done
