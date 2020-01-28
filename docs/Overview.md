  
# CLAI Project Overview

![CLAI](https://www.dropbox.com/s/cuwy4g7xksag0dy/clai-dual.PNG?raw=1)

Project CLAI or Command Line Artificial Intelligence aims to bring the power of AI to the command line. 
Using CLAI, users of Bash can access a wide range of skills that will enhance their command line experience.
The project is intended to rekindle the spirit of AI softbots by providing a plug-and-play framework and simple interface abstractions to the Bash and its underlying operating system. Developers can access the command line through a simple `sense-act` API for rapid prototyping of newer and more complex AI capabilities.

We thus focus on two types of users:

+ End users of the unix command line (e.g. Bash). These are people who use the command line during coding 
and/or in course of usual life in a unix-based operating system. 

+ AI researchers and developers who want to develop `skills` or plugins that can improve life of the end user on the command line. 
There is some overlap between these two types of users -- many skill developers may also be consuming these skills as end users. 

## CLAI for the End User

<img src="https://www.dropbox.com/s/0lupobzbcdfafm4/clai-end-user.png?raw=1" width="400">

Every command that the end user types on the command line is piped through the CLAI infrastrcture instead
of being exectued immediately. This leads to following key changes in how the user interacts with the command line.
*Note that most of the life on command line remains unchanged*, the skills only show up when necessary or 
are specifically invoked.

### Automation

Automate repetitive and menial sequence of commands that achieve tasks on the command line. End users already write scripts to
do this. The value of AI skills is for the user to no longer have to write specific scripts but to be able to instead learn those sequences (reinforcement learning) from observing users and compose skills automatically (planning) to perform even more complicated tasks.

> previously 

```
>> command p
>> command q
>> command r
```

> now

```
>> do task xyz
clai: command p
clai: command q
clai: command r
```

The [`ibmcloud`](../clai/server/plugins/ibmcloud) skill is an example of this in action.

### Support & Troubleshooting

Skills embedded locally can allow support to be: 1) In situ; 2) Immediate; and 3) Personalized 
(i.e. tuned to the local configuration) so that the
end user no longer has to go looking for answers on the internet.
This can allow them to stay in context and be more productive.

> previously 

```
>> command q
Error: xyz
(user leaves CLI to search for answers on the internet)
>> command p
>> command q
```

> now

```
>> command q
Error: xyz
clai: command p
>> command p
>> command q
```

+ **Proactive Troubleshootin:** Support can also be proactive if the skills are given more power. In such cases, the end user does not even feel the error that would have occured in the absense of the skills in the background.

> previously 

```
>> command q
Error: xyz
(user leaves CLI to search for answers on the internet)
>> command p
>> command q
```

> now

```
>> command q
clai: command p
clai: command q
```

The [`man page explorer`](../clai/server/plugins/manpage_agent) [`fixit`](../clai/server/plugins/fix_bot) [`helpme`](../clai/server/plugins/retrieval_agent) [`howdoi`](../clai/server/plugins/search_agent) skills are examples of on-remise immediate support in action.

### Natural Language Support

With natural language support (for now, English only), it may be possible to significantly bring down the expertize needed to work on the command line, while keeping developers in context who no longer have to go looking for [frequently used commands
that no one can remember the parameters of!](https://imgs.xkcd.com/comics/tar.png)

> previously 

```
(user leaves terminal to figure out how to do task xyz)
>> command p
```

> now

```
>> do xyz
clai: command p
>> command p
```

The [`nlc2cmd`](../clai/server/plugins/nlc2cmd) skill is one such example.

Such interaction need not be single turn. Instead the framework allows for holding short converstations 
to figure out stuff for features like **automate** or **troubleshoot** to flourish. 

### Pedagogy 

Finally, we can use the skills to bring up the expertise of the end user over time. As in the previous case,
these interactions are not single turn. Instead bots can work over long periods into, for example, turning new
adopters of cloud platforms into expert developers and deveops.

> previously 

```
>> command p
(stdout/stdin)
```

> now

```
>> command p
(stdout/stdin)
clai: command q is a better way to do this
```

---------------

## CLAI for the AI Developer

<img src="https://www.dropbox.com/s/c26ldu12th7vb1z/clai-developer.png?raw=1" width="500">

Assistants that operate with end users in the space of operating systems has been a pipedream for the AI community for a long time. 
Starting from the infamous Clippy and other "AI Softbots" conceived in the 90s, the dream has remained largely out of reach. 
Part of the problem here has been in the difficulty of the AI researcher in navigating the intricacies of an operating system 
while concentrating on exploring and expanding newer exciting frontiers of research.

We attempt to solve this problem by making the Bash environment available to an AI developer as a generic `environment` API 
(think [OpenAI Gym](http://gym.openai.com/) but for the Bash). 
This allows developers to not have to deal with interfacing to the Bash themselves
and instead focus on building any AI skill they wish. The interface to the Bash environment allows execution of actions
and sensing of the result of those actions in a manner similar to the classic AI agent architecture 
[Russel & Norwig 1995, Sutton 1992] AI researchers are already familiar with.

<img src="https://www.dropbox.com/s/u9ujjgl3gtrkigr/clai-agent-architecture.png?raw=1" width="300">

This setup allows the develop to:

+ **Listen & Learn**: Continuously remain plugged into the terminal, as the user is working on it, to learn from the user's actions and/or keep track of state. 

+ **React**: Respond to specific requests from the user and/or chime in when it has something useful to contribute (e.g. fetch a forum 
post and suggest a fix when the user encounters and error).

+ **Simulate**: Spawn off a container to try out actions in and learn from their results, in a manner similar to [UbuntuWorld](http://rakaposhi.eas.asu.edu/ubuntuworld-iaai17.pdf).

> Note: Each container is a fresh system by default. This does **not** allow making a copy of the current system to simulate effects of actions in real time before suggesting to the end user.

> :hourglass_flowing_sand: This feature is under development.

+ **Orchestrate**: Deal with the response of many skills together in a manner similar to the latest in [IBM Watson Assistant](https://cloud.ibm.com/docs/services/assistant?topic=assistant-skills) or [Amazon Alexa](https://developer.amazon.com/en-US/alexa/alexa-skills-kit) skills.

> Note: This framework does **not** currently allow plugins to react unless a command has been put in by the end user. So, for example, something like intelligent autocomplete is not yet supported. 

-----

**Get started!** &nbsp; [`CLAI API`](../clai/server/plugins/) &nbsp; [`Community on Slack`](http://ibm.biz/clai-slack) &nbsp; [`FAQs`](FAQ.md)
