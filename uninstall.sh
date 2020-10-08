#!/bin/bash -e
flags=""

# Check for user passed args
while test $# != 0
do
  case "$1" in
    --user) 
      USER_INSTALL=true
      flags="$flags --user"
    ;;
    # add more flags here
    *) flags="$flags $1"
  esac
  shift
done

die () {
  echo -e $1;
  exit $2;
}

is_sh () {
  value=$(ps -o args= -p "$$" | cut -f 1 -d " ")
  test "sh" = $value
  return
}

command_exists () {
  type "$1" &> /dev/null ;
}

if is_sh ; then
  die "\n Please don't invoke with sh, to uninstall use ./uninstall.sh"
fi

if [ "$USER_INSTALL" != true ]; then
  if [ "$EUID" -ne 0 ]; then
    die "\n Please run as sudo."  1
  fi
fi

if ! command_exists python3 ; then
  die "\n Sorry you need to have Python3 installed. Please install it and rerun this script."  1
fi

if ps -o args -u `whoami` | grep "[c]lai-run" &> /dev/null ; then
  if [ ! $(uname) == 'OS/390' ] && [ ! $(uname) == 'z/OS' ]; then
    running_process=$(ps -o args -u $(whoami) | grep "[c]lai-run" | head -1)
    pkill -f "${running_process}"
  else
    clai_pid=$(ps -e -o pid,args -u `whoami` | grep "[c]lai-run" | head -1 | awk '{print $1}')
    clai_subpids=$(ps -e -o pid,ppid -u `whoami` | awk '$2=='"$clai_pid"'' | awk '{printf "%s ",$1}')
    kill -9 $clai_pid $clai_subpids
  fi
fi

eval "python3 uninstall.py $flags"
