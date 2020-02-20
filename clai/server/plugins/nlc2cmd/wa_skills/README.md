# nlc2cmd for IBM Cloud CLI

`NLP` `Support` `ibmcloud`

This contains scripts that turn the recognized intents into actionable commands on the command line. 
Previously in [../](../) we looked at some common examples using the `tar` and `grep` commands. 
Here we want to highlight another instantiation of the nlc2cmd use case, this time for the [IBM Cloud CLI](https://www.ibm.com/cloud/cli) and the `ibmcloud` family of commands.

## Example Usage

![nlc2cmd4ibmcloudcli](https://www.dropbox.com/s/35oucoqq4o8pwau/nlc2cloud.gif?raw=1)

The script [cloudbot.py](cloudbot.py) supports some illustrative commands from the [IBM Cloud CLI cheatsheet](https://github.com/ibm-cloud-docs/cli/blob/master/IBM%20Cloud%20CLI%20quick%20reference.pdf) -- CLAI currently handles all these instances. Try them out, or the ones below as a quick start!

1. `>> How do I login?`
2. `>> how do i organize my resources`
3. `>> show me how to add tags`
4. `>> billing costs`
5. `>> available plugins`
6. `>> I want to invite someone to my cloud`

## [xkcd](https://uni.xkcd.com/)

There's planned downtime every night when we turn on the Roomba and it runs over the cord.

![alt text](https://imgs.xkcd.com/comics/the_cloud.png "There's planned downtime every night when we turn on the Roomba and it runs over the cord.")
