## Installing Docker

> **Recommended**: Follow the Docker getting started tutorials online [[link](https://docs.docker.com/get-started/)] to familiarize yourself with Docker. 


### Installing Docker For MacOS
1. Download Docker from [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac). 
2. Sign in to your Docker account or register for a new account. Registration is free and it only requires a valid email address.
3. Once you have successfully downloaded the `Docker.dmg` installer file, open it by double-clicking on it and then drag the
Moby-the-whale icon to the Application folder. Installation will require system privileges.
4. Once installed, double-click `Docker.app` in the Applications folder to start Docker.

### Installing Docker For Linux

You need `docker` and `docker.io` installed on your system.

> For Debian-based systems, type:
```
sudo apt-get install docker docker.io
```

> For Red Hat or CentOS based system, type:
```
sudo yum install docker-ce
```

> For Fedora-based system (version 22 or earlier), type:
```
sudo yum install docker
```

> For Fedora-based system (version 23 or later), type:
```
sudo dnf install docker
```

## Installing Python 3.6

Python 3.6 (or higher) is required to run CLAI. Download and run the Python installer package for your operating system 
from [https://www.python.org/downloads/](https://www.python.org/downloads/).

## Installing Homebrew with fswatch for MacOS

To install Homebrew, execute the following command in your console:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

When prompted, press return to continue, and enter your credentials to begin installation. 
Once Homebrew is successfully installed, execute the following command to install fswatch.

```
brew install fswatch
```
