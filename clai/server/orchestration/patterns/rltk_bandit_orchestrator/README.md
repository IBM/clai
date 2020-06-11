# Bandit-based Orchestration

> :warning: :warning: This orchestration pattern is developed on top of IBM Research's 
internal `rltk` toolkit for reward-based learning and **would not run on general machine**. 
You are welcome to develop with your own favorite ML platform until such time `rltk` 
becomes open source. 

This is an illustration of an orchestration pattern that learns based on user feedback 
using contextual bandits. The context is given by the active skills and their corresponding 
self-reported confidences, while the reward is either received: 

+ directly if the user accepts a suggestion with a `y/n` response 
(e.g. for the `howdoi` or `man page explorer` skills); or 
+ indirectly if they execute a command that follows the suggestion closely 
(e.g. for the `nlc2cmd` or `fixit` skills). 

An orchestration layer that can adapt to user interactions over time allows you to 
develop CLIs that are personalized to the needs of individual users or user types, 
as well as deal with miscalibrated confidences of skills.

Bandits - and Reinforcement Learning based agents in general - require an initial 
phase of exploration which can adversely affect the end-user experience. To bypass
this phase, the bandits can be warm-started with a particular profile. Four profiles
are included in the package:

- `max-orchestrator`: Starts the bandit orchestrator as a max orchestrator. This behavior
then changes over time with the user behavior. 
- `ignore-clai`: Ignores CLAI altogether and treats each command as a native bash command
- `ignore-skill`: Ignores a particular skill while retaining `max-orchestrator` 
behavior for the rest, and
- `prefer-skill`: Prefers one skill over another and is useful in scenarios where a user
prefers one skill from a pool of skills with overlapping domains.

|  Warm-start behavior     |   Preview    |
| ----- | ----- |
| `max-orchestrator` | <img src="https://www.dropbox.com/s/t0s9l066ntfd5v4/max-orchestrator.png?raw=1" />  |
| `ignore-clai` | <img src="https://www.dropbox.com/s/ji8t8mraav9xszh/noop.png?raw=1" />  |
| `ignore-nlc2cmd` | <img src="https://www.dropbox.com/s/a28s965vit3fshj/ignore-nlc2cmd.png?raw=1" />  |
| `prefer-manpage-over-nlc2cmd`   | <img src="https://www.dropbox.com/s/meho56ix1srfe9j/manpage-over-nlc2cmd.png?raw=1" />  |
