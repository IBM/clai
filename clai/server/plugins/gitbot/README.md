# gitbot

`NLP` `Support` `Automation`

This skill lets you manage and organize your github repository in natural language.
It also lets you use natural language commands to issue popular git commands. 

## Implementation

The skill demonstrates hooks into two interesting design patterns:

+ Similar to the [`nlc2cmd`](../nlc2cmd/) skill, it demonstrates natural language to 
command patterns. However, in contrast to the nlc2cmd implementation, here we demonstrate
how to use a natural language classifier local to the machine -- using [RASA](https://rasa.com/) --
instead of calling an external service like [Watson Assistant](https://www.ibm.com/cloud/watson-assistant/). 

+ This skill also demonstrates instances of workflow automation in the context of code 
development by using the [GitHub Actions API](https://github.com/features/actions).

Similar to the `nlc2cmd` and `ibmcloud` skills, this skill is also merely illustrative
of integration of natural language and automation in code management through GitHub.
Contributions are welcome to improve the accuracy of the natural language interpretation,
the breadth of the use cases covered for workflow automation, or new features!

## Example Usage

TODO

<!-- ![nlc2cmd](https://www.dropbox.com/s/ybuwyixqobjo8za/nlc2cmd.gif?raw=1) -->

<!-- Right now this skills only supports `grep` and `tar` commands. Try these out!

1. `>> list all files in this archive`
2. `>> extract all images from the archive into this directory`
3. `>> compress the directory`
4. `>> compress the directory into a bz2 file and print details`
5. `>> what is the size of this archive`
6. `>> grep for all files with "clai" in this directory, show me the line numbers`
7. `>> grep for the number of files with "clai" in this directory`
 -->


## [xkcd](https://uni.xkcd.com/)

If that doesn't fix it, git.txt contains the phone number of a friend of mine who understands git. Just wait through a few minutes of 'It's really pretty simple, just think of branches as...' and eventually you'll learn the commands that will fix everything.

![alt text](https://imgs.xkcd.com/comics/git_2x.png "If that doesn't fix it, git.txt contains the phone number of a friend of mine who understands git. Just wait through a few minutes of 'It's really pretty simple, just think of branches as...' and eventually you'll learn the commands that will fix everything.")
