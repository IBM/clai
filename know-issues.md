#Know Issues

##Fedora

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