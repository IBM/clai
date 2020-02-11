# nlc2cmd for ibmcloud

`NLP` `Support`

This skill lets you specify tasks in English and retrieve their command line syntax. This is a specific instantiation for the `ibmcloud` [starter kit](https://github.com/ibm-cloud-docs/cli/blob/master/IBM%20Cloud%20CLI%20quick%20reference.pdf).

## Implementation

Currently the command typed in by the user is passed through a natural language classifier on 
[Watson Assistant](https://www.ibm.com/cloud/watson-assistant/). 
If there is a significant match with known patterns of `ibmcloud`,
the user command is translated into the corresponding command line syntax [here](./wa_skills/).
The skills confidence is the same as the confidence of the NLC.  

This skill is merely illustrative and can be made as accurate as desired for these
specific use cases. However, this approach would not scale to Bash commands
in general and is quite brittle. See the `nlc2cmd Challenge` below for more on this.

<!-- ## Example Usage

![nlc2cmd](https://www.dropbox.com/s/ybuwyixqobjo8za/nlc2cmd.gif?raw=1)

Right now this skills only supports `grep` and `tar` commands. Try these out!

1. `>> list all files in this archive`
2. `>> extract all images from the archive into this directory`
3. `>> compress the directory`
4. `>> compress the directory into a bz2 file and print details`
5. `>> what is the size of this archive`
6. `>> grep for all files with "clai" in this directory, show me the line numbers`
7. `>> grep for the number of files with "clai" in this directory` -->

## :star: :star: :star: :star: :star: `nlc2cmd Challenge`

No one remembers arcane flags to commands we use every day.
The ability to turn natural language instructions to bash commands has been a pipe 
dream for the research community for a while. 
After all, there is a lot of data already out there in public forums and in documentation
that can be readily leveraged. 
Especially with recent advances in natural language processing, 
this problem has received renewed interest.

> Check out [Betty](https://github.com/pickhardt/betty).

> **NL2Bash: A Corpus and Semantic Parser for Natural Language Interface to the Linux Operating System.**
Xi Victoria Lin, Chenglong Wang, Luke Zettlemoyer, Michael D. Ernst. 
The 11th International Conference on Language Resources and Evaluation, 2018.

Most recent attempts (including the ones above) are either heavily rule based or 
do not scale beyond the examples that can be mined reliably from forums. 
As such, it remains an open challenge today.

As part of Project CLAI, we intend to curate and release an open dataset around this 
challenge and host a leaderboard of competing solutions. 
Contribute [here](https://forms.gle/MXWfGYCtiVDNfNdU8).

## xkcd
I don't know what's worse--the fact that after 15 years of using tar I still can't keep the flags straight, or that after 15 years of technological advancement I'm still mucking with tar flags that were 15 years old when I started. 

![alt text](https://imgs.xkcd.com/comics/the_cloud.png "There's planned downtime every night when we turn on the Roomba and it runs over the cord.")
