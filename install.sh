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

UNAME=$(uname -s)

command_exists () {
  type "$1" &> /dev/null ;
}

if is_sh ; then
  die "\n Please don't invoke with sh, install use ./install.sh"
fi

if [ "$USER_INSTALL" != true ]; then
  if [ "$EUID" -ne 0 ]; then
    die "\n Please run as sudo."  1
  fi
fi

if ! command_exists python3 ; then
    die "\n Sorry you need to have Python3 installed. Please install it and rerun this script."  1
fi

if [ "$UNAME" = "Darwin" ]; then
    if ! command_exists brew ; then
        die "\n Sorry you need to have brew installed. Please install it and rerun this script."  1
    fi
fi

if lsof -i -P -n | grep 8010 > /dev/null 2>&1; then
  die "\n Another process is running on port 8010."
fi

if [ "$USER_INSTALL" == true ]; then
  python3 -m pip install --user -r requirements.txt
else
  python3 -m pip install -r requirements.txt --ignore-installed
fi

python3 -m pip install --upgrade keyrings.alt
python3 install.py $flags --shell bash