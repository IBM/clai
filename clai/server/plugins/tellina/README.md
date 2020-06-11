# tellina

`NLP` `Support`

This skill expands on the functionality of the [`nlc2cmd`](https://github.com/IBM/clai/tree/master/clai/server/plugins/nlc2cmd) skill by 
providing a direct interface to the [`Tellina`](https://github.com/TellinaTool/) system. 

## Implementation

The natural language input from the user at the command line is sent as a query to an 
instance of the [`Tellina`](http://tellina.rocks/) system, which runs [`NL2Bash`](https://github.com/TellinaTool/nl2bash/) as its 
translation engine. `NL2Bash` uses [`TensorFlow`](https://www.tensorflow.org/) to create a model of the top `Bash` [*utilities*](https://github.com/TellinaTool/nl2bash/tree/master/data/bash), and predicts a relevant utility for the user's natural language query. After that, it uses *Abstract Syntax Trees* (ASTs) to predict the correct options (flags) to use with that predicted utility. 

### Scoring & Confidence

Currently, the `tellina` skill returns a default confidence of `0.0`. We are working on a confidence scoring function that retrieves the prediction probabilities from TensorFlow and converts them into a confidence score for use with `CLAI`. 

Use direct invocation to use `tellina` even with zero confidence.

```
>> clai "tellina" [command]
```

## Example Usage

![clai-tellina-gif](https://www.dropbox.com/s/063tmajzchskvws/tellina.gif?raw=1)

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

## :star: NeurIPS 2020 NLC2CMD Competition

We are excited to announce the [`NeurIPS 2020 NLC2CMD competition`](http://ibm.biz/nlc2cmd), which builds on Tellina and the NL2Bash data. To sign-up for the competition, click [here](http://nlc2cmd.us-east.mybluemix.net/#/participate)! 

## [xkcd](https://uni.xkcd.com/)


The pile gets soaked with data and starts to get mushy over time, so it's technically recurrent.  

![alt text](https://imgs.xkcd.com/comics/machine_learning.png "The pile gets soaked with data and starts to get mushy over time, so it's technically recurrent.")
