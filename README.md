![CLAI Logo](https://www.dropbox.com/s/nbkfa59khtlcs79/clai-logo.png?raw=1)

Command Line Artificial Intelligence `CLAI` is an open-sourced project aimed to bring the power of AI to the command line. Using CLAI, users of Bash can access a wide range of skills that will enhance their command line experience. This repository contains the source code and documentation to get you started.

## Getting Started

[`Home`](https://clai-home.mybluemix.net/) &nbsp;  See some example use cases without installing or building anything locally. A great way to try out CLAI as a first step!

[`More`](docs/Overview.md) &nbsp; [`API`](clai/server/plugins/) &nbsp;   This link describes the functional plugins that enable the different kinds of interaction that we call skills.

[`Community`](http://ibm.biz/clai-slack) &nbsp;  Join our online Slack community by clicking here!

[`FAQs`](docs/FAQ.md) &nbsp;  Frequently Asked Questions including those about Security and other commonly asked about topics.

[`Whitepaper`](https://arxiv.org/abs/2002.00762) &nbsp;  A research architecture paper describing how this all works.

[`Blog`](https://www.ibm.com/blogs/research/2020/02/bringing-ai-to-the-command-line/) &nbsp;  The initial public release about this project.

[`Feedback`](http://ibm.biz/clai-survey) This link is a survey to help us improve our project going forward!

### Prerequisites

+ `Bash`
+ `Python 3.6` or higher
+ `Homebrew` + `fswatch` if you are working on MacOS
+ `Docker` if you are using the containerized version of CLAI (see below)

### Installing CLAI Natively

1. Open a Bash emulator or console.
2. In the console navigate to the location of the CLAI project source code.
3. Execute the following:

```
$ sudo ./install.sh
```

**In Fedora, Debian and Ubuntu**, you need to install with this extra parameter:

```
$ sudo env "HOME=$HOME" ./install.sh
```

After the installation is complete, you will be prompted to restart the shell before CLAI becomes active.

#### Uninstalling CLAI

To uninstall CLAI, execute the following command from the directory hosting the CLAI source code:

```
$ sudo ./uninstall.sh
```
**In Fedora, Debian and Ubuntu**, you need to uninstall with this extra parameter:

```
$ sudo env "HOME=$HOME" ./uninstall.sh
```

As before, during installation, you will have to restart the shell for the changes to take effect.

### Bringing up CLAI in a container

Follow these steps to try out CLAI inside a containerized environment. This may be useful while you are developing bots for CLAI or if you want to try out CLAI without affecting your host system. Start by building the Docker container as follows:

**Mac OS**
```
$ ./BuildDockerImage.sh
```

**Fedora and Ubuntu**
```
$ sudo ./BuildDockerImage.sh
```

The end of a successful build process (this can take a while) should resemble the following output:

```
CLAI has been installed correctly, you need restart your shell.
Removing intermediate container 1644ed9c1046
 ---> b653fa2f2114
Successfully built b653fa2f2114
Successfully tagged claiplayground:latest

real	4m4.184s
user	0m0.309s
sys	0m0.271s
```

Once you have built the Docker image, you can run it locally or on a remote server with a copy of the docker image, by executing the following launch script. This script starts the CLAI-enabled container and sets up SSH forwarding from the physical host to the container.

**Mac OS**
```
$ ./RunDockerImage.sh
f61ce8a1c049f54d3a7fb8df5d00612d5c86f8c164049d0819c5fefea4142c7e
```

**Fedora and Ubuntu**
```
$ sudo ./RunDockerImage.sh
f61ce8a1c049f54d3a7fb8df5d00612d5c86f8c164049d0819c5fefea4142c7e
```

You can determine what port your docker container is using (numbers marked between asterisks) for the SSH server as follows. Note that the port is assigned automatically and will be distinct for each docker instance you are testing.

**Mac OS**
```
$ docker ps -a
CONTAINER ID   IMAGE               COMMAND            CREATED   STATUS   PORTS              NAMES
f61ce8a1c049   claiplayground   "/usr/sbin/init"   ---       ---      0.0.0.0:*32782*-   trusting_blackburn
```

**Fedora and Ubuntu**
```
$ sudo docker ps -a
CONTAINER ID   IMAGE               COMMAND            CREATED   STATUS   PORTS              NAMES
f61ce8a1c049   claiplayground   "/usr/sbin/init"   ---       ---      0.0.0.0:*32782*-   trusting_blackburn
```

Now you are ready to ssh into the docker container.

```
$ ssh root@localhost -p *32782* <--- replace by port number from above
The authenticity of host '[localhost]:32782 ([::1]:32782)' can't be established.
ECDSA key fingerprint is SHA256:dGxCC2kikyWVoRk9RHXgVvJUZoMHiFM8AQfF4wjhd38.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[localhost]:32782' (ECDSA) to the list of known hosts.
root@localhost's password:
...
Research Docker Build.
nohup: appending output to ‘nohup.out’
[root@f61ce8a1c049 ~]#
```

## Interacting with CLAI

If you are not already in Bash, go into Bash by typing `>> bash`. You can continue interacting with a CLAI-enabled Bash as you would normally with Bash. At the core of CLAI is a set of skills that will show up in your interactions with the terminal if they are confident that they can improve your command line experience.

At any time, you can list the active skills by typing:

```
$ clai skills
```

You can activate (and install) a skill specifically by invoking:

```
$ clai activate <skill-name>
```

You can also start or stop the CLAI support as follows:

```
$ clai stop
$ clai start
```

> **Warning:** If you attempt to stop CLAI and start it again too rapidly, it is posible that you have to wait several seconds for internal process cleanup (socket closing and recycling) before the CLAI process will start completely.

### Configuring CLAI

If you want to allow CLAI to automatically execute commands without your explicit authorization and interaction, you can use the `auto` directive. Issuing the command again will toggle the auto-user mode on and off.

```
$ clai auto
```

If you wish to set which plugins are activated by default,
you can set them in [`configPluging.json`](configPlugins.json)
as follows:

```
{ ..., "default": ["skill_name_1", "skill_name_2", "skill_name_3"], ...}
```

You will need to reinstall CLAI and restart your shell for the changes to take effect.

## Interaction Patterns

Your life on the terminal remains largely unaffected unless required by you or
in reponsed to an error. Specifically, there are three ways in which CLAI skills may be invoked.

+ `$ command` This is usual life on Bash. A skill may or may not show up in the standard interaction 
depending on their self-determined confidence of their usefulness in the context of that interaction.
+ `$ clai command` This will invoke the CLAI skill with the highest confidence *regardless of their confidence*. 
Use this if you want to force CLAI to respond. 
+ `$ clai "skill-name" command` This will invoke the given skill name *regardless of its own confidence and the
confidences of the other active skills*. Use this if you want to force a particular skill in CLAI to respond. 

In all three cases, the Bash will behave as normal if CLAI has nothing to respond.
Generally, there are two ways in which a skill will come alive, as we describe next.

### Response to Commands

A skill can respond to your command directly:

+ This could be an answer or command in response to something you typed into the terminal in natural language.
+ This could be an augmenation or fix to your command to make it work as intended.

Without the `auto` option (see above), a CLAI skill will *always* ask for your permission before executing an action
on its own on your terminal.

### Response to Execution

A skill can also respond the execution of your command:

+ This could be an addition to the `stdout` to provide you useful information about your task.
+ This could be a response to an `stderr` with a suggestion to fix the error or with useful troubleshooting information.

As before, CLAI skill will not execute without your permission unless `auto` mode is **on**.

## :robot: Want to build your own skills?

[`fixit`](clai/server/plugins/fix_bot) &nbsp; [`nlc2cmd`](clai/server/plugins/nlc2cmd) &nbsp; [`helpme`](clai/server/plugins/helpme) &nbsp; [`howdoi`](clai/server/plugins/howdoi) &nbsp; [`man page explorer`](clai/server/plugins/manpage_agent) &nbsp; [`ibmcloud`](clai/server/plugins/ibmcloud)  

Project CLAI is intended to rekindle the spirit of AI softbots by providing a plug-and-play framework and simple interface abstractions to the Bash and its underlying operating system. Developers can access the command line through a simple `sense-act` API for rapid prototyping of newer and more complex AI capabilities.

Want to build your own skills? Get started with the [`CLAI API`](clai/server/plugins/) now!

---------------

The CLAI logo is available under the [`Free Art License`](http://artlibre.org/licence/lal/en/). It has been adopted and modified from the [`Bash logo`](https://github.com/odb/official-bash-logo).
