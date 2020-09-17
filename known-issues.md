# Known Issues

## Fedora

Fedora by default doesn't have Python3 and Pip3 installed. And the install process need install pythondev for install some packages.

If you does not have Python installed we recomend to you execute

```commandline
    sudo dnf install python37
    sudo dnf install python3-devel
```

After that test that everything is correctly installed checking the version with

```commandline
>> python3 -V 
    Python 3.7.5
>> pip3 -V
    pip 19.0.3 from /usr/lib/python3.7/site-packages/pip (python 3.7)
```

Sometimes pip3 is redirected to other path and old version. For fixing that invoke

```commandline
sudo rm -rf <path_wrong_version>
```

## z/OS

There are numerous problems with the (multiple competing) ports of Python to
z/OS.  All versions of z/OS Python routinely regress, often introducing,
resolving, then later re-introducing character encoding problems.  Furthermore,
an install process that worked on one level of Pip may not work with a
subsequent level of Pip.  Its a mess.

One "known good" path to installing CLAI on z/OS is to use Bash 4.3, Python 3.6
from IzODA, and a backlevel version of Pip3 (such as v9.0.1).  You can perform
installation using the instructions in [README.md](README.md), or you can run

```commandline
(bash-4.3)USERID@ZOSYS:~> cd clai
(bash-4.3)USERID@ZOSYS:~/clai> make clean
(bash-4.3)USERID@ZOSYS:~/clai> make install
```