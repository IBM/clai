# Troubleshooting

## Known issue with Python and Bash on the CLAI-enabled Shell

Currently, we do not support going into a recursive Bash session or the interactive python shell from inside a CLAI-enabled terminal. If you type in `>> bash` your current shell window will freeze, and if you move into the python shell, you will not be able to see the stdout and stderr until you come out of it. 

## Known issue with parentheses in commands

The CLAI server crashes when commands have parentheses: e.g. `(ls | grep hi) | grep .`. We intend to support more and more complex invocations such as these in future releases. 

## Installation Error with Homebrew

```
Error: Running Homebrew as root is extremely dangerous and no longer supported.
As Homebrew does not drop privileges on installation you would be giving all
build scripts full access to your system
```

You may not use Homebrew during the installation of any component if it requires sudo access... you will notice this :point_up: error. Brew no longer supports `sudo`. Installation scripts for individual skills do not use sudo and hence do support brew (instructions that require sudo, such as `pip`, need to be invoked with sudo inside the installation script).

## Python / Pip not found

### Fedora

Fedora does not have Python3 and Pip3 installed by default. If you do not have Python installed we recomend you execute:

```commandline
>> sudo dnf install python37
>> sudo dnf install python3-devel
```

You can test that everything is correctly installed by checking the version with:

```commandline
>> python3 -V 
Python 3.7.5
>> pip3 -V
pip 19.0.3 from /usr/lib/python3.7/site-packages/pip (python 3.7)
```

Sometimes Pip3 is redirected to a different path and an older version. For fixing that, invoke:

```commandline
>> sudo rm -rf <path_wrong_version>
```

### Ubuntu

Similar to Fedora, you may need to install Python3 and Pip3

```commandline
>> sudo apt update 
>> sudo apt install python3.6 
>> sudo apt install python3-pip
```
