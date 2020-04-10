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

## Docker on Windows

In some cases when attempting to run clai within a docker container, all bash scripts will be unable to run due to windows changing the line break character from `\n` to `\r\n`. 

To resolve this in the docker container first we must uninstall the broken clai instance by running:

*note: we use the python script directly rather than the shell script which is currently broken*

```
sudo python3 ./uninstall.py
```

Next, we install a package to convert the line breaks for us:

```
sudo yum install dos2unix -y
```

Now that we have the package lets run it on the contents of the repo. Run the following in the root of the repo:

```
dos2unix $(find . -type f)
```

Finally, we can reinstall clai:

```
sudo ./install.sh
```
