# nlc2cmd

`NLP` `Support`

This skill lets you specify tasks in English and retrieve their command line syntax. 
Currently supported tasks include compressing and uncompress archives 
using `tar` and looking for strings in files using `grep`.

## Implementation

Currently the command typed in by the user is passed through a natural language classifier on
[Watson Assistant](https://www.ibm.com/cloud/watson-assistant/).
If there is a significant match with known patterns of `tar` and `grep`,
the user command is translated into the corresponding command line syntax [here](./wa_skills/).
The confidence of the skill is the same as the confidence of the underlying NLC layer.

This skill is merely illustrative and can be made as accurate as desired for these
specific use cases. However, this approach would not scale to Bash commands
in general and is quite brittle.
Check out the [`NLC2CMD Challenge`](https://ibm.biz/nlc2cmd) @ Neurips 2020.

## Example Usage

![nlc2cmd](https://www.dropbox.com/s/ybuwyixqobjo8za/nlc2cmd.gif?raw=1)

Right now this skills only supports `grep` and `tar` commands. Try these out!

1. `>> list all files in this archive`
2. `>> extract all images from the archive into this directory`
3. `>> compress the directory`
4. `>> compress the directory into a bz2 file and print details`
5. `>> what is the size of this archive`
6. `>> grep for all files with "clai" in this directory, show me the line numbers`
7. `>> grep for the number of files with "clai" in this directory`

See [here](./wa_skills/) for some more examples on the [IBM Cloud CLI](https://www.ibm.com/cloud/cli).


## [xkcd](https://uni.xkcd.com/)

I don't know what's worse--the fact that after 15 years of using tar I still can't keep the flags straight, or that after 15 years of technological advancement I'm still mucking with tar flags that were 15 years old when I started.

![alt text](https://imgs.xkcd.com/comics/tar.png "I don't know what's worse--the fact that after 15 years of using tar I still can't keep the flags straight, or that after 15 years of technological advancement I'm still mucking with tar flags that were 15 years old when I started.")