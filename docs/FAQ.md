# Frequently Asked Questions

## How do I contribute?

Welcome to the world of command line AI. You can contribute in any form, inlcuding adding new features, improving documentation, fixing bugs, or writing new tutorials, and of course, making new skills to add to the CLAI catalog. Please check [here](../CONTRIBUTING.md) for guidelines on contributing code. Also, check out our [Slack](http://ibm.biz/clai-slack) community and join in on the fun!

## What data is being saved?

If you agree to contribute your data during the installation process (optional) we will store 1) statistics on which skills you use; and 2) the `State` and `Action` information outlined [here](../clai/server/plugins/). This will help us improve over time. The data from (2) can be used to train learning agents such as the one outlined [here](../clai/server/orchestration/patterns/bandit_orchestrator/) and may be made available in anonymized form for the community to use as training data. Individual skills do no store any data, unless otherwise mentioned explicitly while they are being installed.

### Do passwords get sent to the skills? 

Note that this framework does not include passwords, and other confidential information, typed into the command line during an interactive execution, to be sent to the skills and to external services. The information in the State object is the one when the command is invoked. This means that if the user does type in the password as part of the command, e.g. `sudo -pass <my_pass>`, then that information *will* be sent.

## Local versus external services: pros and cons?

As you might have noticed, some of the skills call to external services, such as Watson Assistant, to invoke, for example, a natural language classifier. In general, whether to use a local service versus a local one, is left to the discretion of the developer of the skills. We may ideally want skills to be local as much as possible due to variety of reasons: 1) latency: local skills are significantly faster in being able to avoid the call to a remote service; 2) machines are not always connected to the internet so local skills will work more often than remote ones; and 3) being local allows you to customize to the needs of the local machine much more than a general external service that all skills are calling on -- this, of course, makes the best case for having an on-premise assistant such as CLAI embedded on your local terminal. 

One disadvantage of a local service is that they are typically more troublesome to install due to local dependencies (these should be lsited as requirements for the skill). So we kept the default illustrative skills rely primarily on remote services so most developers can try them out with the least overhead.

