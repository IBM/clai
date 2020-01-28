# Bandit-based Orchestration

> :warning: :warning: This orchestration pattern is developed on top of IBM Research's internal `rltk` toolkit for reward-based learning and **would not run on your machine**. You are welcome to develop with your own favorite ML platform until such time `rltk` becomes open source. 

This is an illustration of an orchestration pattern that learns based on user feedback using contextual bandits. 
The context is given by the active skills and their corresponding self-reported confidences, while the reward
is either received: 

+ directly if the user accepts a suggestion with a `y/n` response (e.g. for the `howdoi` or `man page explorer` skills); or 
+ indirectly if they execute a command that follows the suggestion closely (e.g. for the `nlc2cmd` or `fixit` skills). 

An orchestration layer that can adapt to user interactions over time allows you to develop CLIs that are 
personalized to the needs of individual users or user types, as well as deal with miscalibrated 
condifences of skills.
