# gpt3 `OpenAI API` 

`NLP` `Support`

This skill mirrors the [`tellina`](https://github.com/IBM/clai/tree/master/clai/server/plugins/tellina) skill,
and the [NLC2CMD](http://ibm.biz/nlc2cmd) use case, but uses the recently released GPT-3 model instead. 

## Implementation

The skill makes a remote call to the [OpenAI API](https://openai.com/blog/openai-api/), apply 
for yours [here](https://forms.office.com/Pages/ResponsePage.aspx?id=VsqMpNrmTkioFJyEllK8s0v5E5gdyQhOuZCXNuMR8i1UQjFWVTVUVEpGNkg3U1FNRDVVRFg3U0w4Vi4u). 

The setup uses the GPT-3 utility in CLAI, please refer to the 
instructions [here](https://github.com/IBM/clai/tree/master/clai/server/utilities/gpt3) for more details. 

### Scoring & Confidence

Currently, the `gpt3` skill returns a default confidence of `0.0`. Use direct invocation to use `gpt3`. If you have ideas to score and explain the responses from the GPT-3 model, open a PR! 


```
>> clai "gpt3" [command]
```

## Example Usage

![clai-gpt3-snapshot](https://user-images.githubusercontent.com/4764242/88873573-eef7ef80-d1ea-11ea-94c5-06d65b06bf4e.png)


## [xkcd](https://uni.xkcd.com/)


The pile gets soaked with data and starts to get mushy over time, so it's technically recurrent.  

![alt text](https://imgs.xkcd.com/comics/machine_learning.png "The pile gets soaked with data and starts to get mushy over time, so it's technically recurrent.")
