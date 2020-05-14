# Tellina

`NLP` `Support`

This skill expands on the functionality of the [`nlc2cmd`](../nlc2cmd) skill by with a more generic natural language
classification layer that extends to more Bash commands in general.

## Implementation and Example Usage

The skill makes an external call to an instance of the [Tellina](http://kirin.cs.washington.edu:8000/) server which serves the [`NL2Bash`](https://www.aclweb.org/anthology/L18-1491.pdf) [`Github`](https://github.com/TellinaTool/nl2bash) approach for translating English commands to Bash syntax.
Find more examples usages here: [http://tellina.rocks/](http://tellina.rocks/).

The translator is based on [Seq2Seq](https://arxiv.org/abs/1409.0473) and [CopyNet](https://arxiv.org/abs/1603.06393) models.
This will be used as the baseline for the [`NLC2CMD Challenge`](https://ibm.biz/nlc2cmd) @ Neurips 2020.

>* NL2Bash: A Corpus and Semantic Parser for Natural Language Interface to the Linux Operating System. Xi Victoria Lin, Chenglong Wang, Luke Zettlemoyer, Michael D. Ernst. The 11th International Conference on Language Resources and Evaluation, 2018.

## [xkcd](https://uni.xkcd.com/)

I don't know what's worse--the fact that after 15 years of using tar I still can't keep the flags straight, or that after 15 years of technological advancement I'm still mucking with tar flags that were 15 years old when I started.  

![alt text](https://imgs.xkcd.com/comics/tar.png "I don't know what's worse--the fact that after 15 years of using tar I still can't keep the flags straight, or that after 15 years of technological advancement I'm still mucking with tar flags that were 15 years old when I started.")
