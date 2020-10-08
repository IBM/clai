# Known Issues

## Fedora

Fedora by default doesn't have Python3 and Pip3 installed. And the install process need install pythondev for install some packages.

If you does not have Python installed we recommend to you execute

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

### "Known Good" Python Configurations

The best results we've had in installing CLAI on z/OS were with IBM Open
Enterprise Python for z/OS 3.8, using Pip3 >= 20.0.0.

The following additional configurations are known to work to some degree or
another:

+ IzODA Python 3.6, but only with a backlevel Pip3 (verified with Pip3 v9.0.1)

With any of the above configurations, you can perform installation using the
instructions in [README.md](README.md), or you can run:

```commandline
(bash-4.3)USERID@ZOSYS:~> cd clai
(bash-4.3)USERID@ZOSYS:~/clai> make clean
(bash-4.3)USERID@ZOSYS:~/clai> make install
```

### Known Problems

#### General

+ The path to the env program must be `/usr/bin/env`
  - If this is not the case, your system administrator will need to create a symbolic link: `ln -s /bin/env /usr/bin/env`

#### IzODA Python 3.6

+ In order for install/uninstall to work properly your `.bashrc` and
  `.bash_profile` files must be tagged either `ISO8859-1` or `IBM-1047`
  beforehand
+ The `zmsgcode` plugin fails to work due to an SSL validation failure
