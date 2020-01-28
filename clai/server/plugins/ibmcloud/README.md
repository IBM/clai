# ibmcloud

`Automation` &nbsp; `Planning` &nbsp; `Reinforcement Learning` &nbsp; `NLP`

# Implementation

This skill provides an example of automation and support for the deployment pipeline of applications to cloud platforms such as IBM Cloud. The skills maintains state and calls an external planner to generate the pipeline on the fly.

+ A toy domain for deploying a dockerized application to the IBM cloud is available [here](planning-files). The task is modeled as a planning problem and needs to be specified by a domain expert.
+ An [external service](modeled as a planning problem ) uses the [`FAST-DOWNWARD`](http://www.fast-downward.org/) planner to compute a
solution to the specified task, based on the current state of the system and the user command.

![ibmcloud-s2](https://www.dropbox.com/s/dk1fuiulzwymqs1/ss2.png?raw=1)

+ The skill also illustrates how a preliminary execution monitor can be built [here](). We use [`pr2plan`]() to monitor user activity and so that the current state of the system is reflected in the computed solution. For example, here we have asked the skill to run the Dockerfile locally first and so the deployment pipepline no longer needs to build the application again.

![ibmcloud-s1](https://www.dropbox.com/s/0df60ceiihgv8o0/ss1.png?raw=1)

While this skill illustrates an integration of automated planning technologies into user interactions on the command line, the toy domain is written manually now. This approach is unlikely to scale to more complex domains. However, the CLAI API allows one to learn this by observing the user(s) over time. We hope to release datasets and challenges around this task in the future. Watch this space!

## Example Usage

![ibmcloud-gif](https://www.dropbox.com/s/jhjw7l9a7bjvo6k/ibmcloud.gif?raw=1)

Try this out (folllow instructions as they show up):

1. `>> run Dockerfile`  
2. `>> build yaml`  
3. `>> deploy Dockerfile to kube`  

## [xkcd](https://uni.xkcd.com/)
All services are microservices if you ignore most of their features.

![alt text](https://imgs.xkcd.com/comics/containers.png "All services are microservices if you ignore most of their features.")
