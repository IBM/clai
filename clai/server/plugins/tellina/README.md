# Tellina

`NLP` `Support`

This skill expands on the functionality of the [`nlc2cmd`](https://github.com/IBM/clai/tree/master/clai/server/plugins/nlc2cmd) skill by 
providing a direct interface to the [`NL2Bash`](https://github.com/TellinaTool/nl2bash) system. 

## Implementation

The natural language input from the user at the command line is sent as a query to an 
instance of the [`Tellina`](http://tellina.rocks/) system, which runs `NL2Bash` at its 
translation engine. `NL2Bash` uses `TensorFlow` to create a model of the top `Bash` commands, 
and translates a user's natural language query into potential `Bash` commands.

### Scoring & Confidence

Coming Soon

## Example Usage

Coming Soon

### Sample Invocations

## :star: :star: :star: :star: :star: nlc2cmd Challenge

No one remembers arcane flags to commands we use every day.
The ability to turn natural language instructions to bash commands has been a pipe 
dream for the research community for a while. 
After all, there is a lot of data already out there in public forums and in documentation
that can be readily leveraged. 
Especially with recent advances in natural language processing, 
this problem has received renewed interest.

> **NL2Bash: A Corpus and Semantic Parser for Natural Language Interface to the Linux Operating System.**
Xi Victoria Lin, Chenglong Wang, Luke Zettlemoyer, Michael D. Ernst. 
The 11th International Conference on Language Resources and Evaluation, 2018.
Check out [NL2Bash](https://github.com/TellinaTool/nl2bash).

> Check out [Betty](https://github.com/pickhardt/betty), a ''friendly English-like interface for your command line''.

Most recent attempts (including the ones above) are either heavily rule based or 
do not scale beyond the examples that can be mined reliably from forums. 
As such, it remains an open challenge today.

As part of Project CLAI, we intend to curate and release an open dataset around this 
challenge and host a leaderboard of competing solutions. 
Contribute [here](https://forms.gle/MXWfGYCtiVDNfNdU8).


## [xkcd](https://uni.xkcd.com/)


The pile gets soaked with data and starts to get mushy over time, so it's technically recurrent.  

![alt text](https://imgs.xkcd.com/comics/machine_learning.png "The pile gets soaked with data and starts to get mushy over time, so it's technically recurrent.")
