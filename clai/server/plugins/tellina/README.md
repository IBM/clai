# Tellina

`NLP` `Support`

This skill expands on the functionality of the [`nlc2cmd`](https://github.com/IBM/clai/tree/master/clai/server/plugins/nlc2cmd) skill by 
providing a direct interface to the [`Tellina`](https://github.com/TellinaTool/) system. 

## Implementation

The natural language input from the user at the command line is sent as a query to an 
instance of the [`Tellina`](http://tellina.rocks/) system, which runs [`NL2Bash`](https://github.com/TellinaTool/nl2bash/) as its 
translation engine. `NL2Bash` uses [`TensorFlow`](https://www.tensorflow.org/) to create a model of the top `Bash` [*utilities*](https://github.com/TellinaTool/nl2bash/tree/master/data/bash), and predicts a relevant utility for the user's natural language query. After that, it uses *Abstract Syntax Trees* (ASTs) to predict the correct options (flags) to use with that predicted utility. 

### Scoring & Confidence

Currently, the `tellina` skill returns a default confidence of `0.0`. We are working on 
<!-- an implementation of  -->
a confidence scoring function that retrieves the prediction probabilities from TensorFlow and converts them into a confidence score for use with `CLAI`. 

## Example Usage

![clai-tellina-gif](https://ibm.box.com/v/clai-tellina-gif)

### Sample Invocations

Try out the invocations below for a quick start!

1. `>> clai show me all files`
2. `>> clai display files sorted by number of lines`
3. `>> clai tellina show me all running processes`
4. `>> clai print largest files`
5. `>> clai print space separated numbers from 1 to 5`
6. `>> clai recursively add ".jpg" to all files in the current directory tree`
7. `>> clai number of lines in "foo.txt"`
8. `>> clai exit terminal`

The [NL2Bash data](https://github.com/TellinaTool/nl2bash/blob/master/data/bash/all.nl) features an extensive list of natural language invocations that can be used with the Tellina system. 



<!-- ## :star: :star: :star: :star: :star: nlc2cmd Challenge -->
## :star: :star: NeurIPS 2020 NLC2CMD Competition

We are excited to announce the [`NeurIPS 2020 NLC2CMD competition`](http://ibm.biz/nlc2cmd), which builds on Tellina and the NL2Bash data. To sign-up for the competition, [click here](http://nlc2cmd.us-east.mybluemix.net/#/participate)! 

<!-- No one remembers arcane flags to commands we use every day.
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
Contribute [here](https://forms.gle/MXWfGYCtiVDNfNdU8). -->


## [xkcd](https://uni.xkcd.com/)


The pile gets soaked with data and starts to get mushy over time, so it's technically recurrent.  

![alt text](https://imgs.xkcd.com/comics/machine_learning.png "The pile gets soaked with data and starts to get mushy over time, so it's technically recurrent.")
