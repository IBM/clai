# CLAI for the Skill Developer

This is the Python3 API for developing skills for CLAI. Before attempting to make new skills, please read the [overview](../../../docs/Overview.md) of the role of skills in the CLAI Porject and the [description](../../../README.md) of the end user experience. Have fun!

:heavy_check_mark: Make sure to use the skills provided in this directory as examples as you follow along with the instructions.

## Anatomy of a Skill

Every skill you want to make available to CLAI is housed in this directory. 

```
<root>
- clai
  + tools
  + emulator
  ...
  - server
    + command_runner
    ...
    - plugins
      - skill_1
        - manifest.properties
        - install.sh
        - skill_1.py
      + skill_2
      + skill_3
      ...
+ docs
+ bin
+ scripts
...
```

Each skills is contained in its folder which **must** have the following structure:

### The Manifest

A `manifest.properties` file which documents the name, a brief description, and the default installation status 
of the skill. Here is an [example](nlc2cmd/manifest.properties).

```
[DEFAULT]
name=dummy skill
description=This is a dummy skill
exclude=Linux Darwin
default=no
```

+ **name:** This is the name your skills will appears as when the user hits `>> clai skills` on the Bash.
+ **description:** This is a text description of your skill. Supports ASCII.
+ **exclude:** This is a list of operating systems (separated by spaces) to exclude installing the skill in. If you write the name of the OS here, the skill will not appear in it. The OS name are Darwin for Mac and Linux for Linux.
+ **default:** This is **yes** or **no** depending on whether they are installed by default when CLAI is installed. 
    + If the skill requires an installer (see next) and the default option is set to **yes**, then the installation script
will be executed at the time of installation of the CLAI package.
    + Note that this option only dictates whether the skill is installed during the installation of CLAI or not, 
and is separate from the "default" list of skills in [configPlugins.json](../../../configPlugins.json) file which dicates which ones are selected as active when a CLAI-enabled bash session starts. Of course, if a skill is to be selected, it has to be installed as well and so, in that case, this setting **should be set to yes**. 

### Installer

An `install.sh` file that installs all dependencies required by this skill. Here is an [example](nlc2cmd/install.sh).

> **Warning:** If your skill takes a while to install, it may be better to keep it out of the default install list.

### Code

Finally the main python file that houses your skill should match the folder name (here is an [example](nlc2cmd/nlc2cmd.py)).
The class name for your skill can be any name as long as it inherits the `Agent` class. 
We will now go into details of this `Agent` API which implements a `sense-act` cycle with two major components: a `State` and an `Action`.

## States and Actions

The `State` object contains information about the system, including state of the shell, 
system memory, connectivity, file system, etc. as the state information or percept
received from the terminal session that a skill is plugged into.
It has the following information:

| property | type | default | description |
|----------|------|---------|-------------|
| user_name | str | n/a | user name of the user on the terminal |
| command | str | None  | current command entered by the user | 
| root | bool | False | is user using root permissions |
| processes | list | None | list of active processes |
| file_changes | list | None | list of file changes |
| network | list | None | list of active network connections |
| result_code | str | None | result code from last execution |
| stderr | str | None | `stderr` from last execution |
| stdout | str | None | `stdout` from last execution :warning: **Pending** |

The `Action` object, on the other hand, is the directive from the skill to terminal.
It has the following parameters.

| parameters | type | optional | default | description |
|------------|------|----------|---------|-------------|
| suggested_command | str | no | None | command being suggested by the skill |
| description | str | yes | None | a description to attach to `stdout` |
| explanation | str | yes | None | an explanation if available for the suggestion |
| confidence | float | no | 0.0 | self-determined confidence for the suggestion |
| execute | bool | yes | False | permission to execute without user intervention |
| agent_owner | str | no | None | name of skill invoking the action |

+ If you want to not suggest any command, you need to specify `NOOP_COMMAND` as done [here](nlc2cmd/nlc2cmd.py#L18).
+ If the [power mode](../../../README.md) is turned on, then the suggestion will directly lead 
to execution if the `execute` flag is **True**.

### Formatting the CLAI output

We support utf8 text and Unix color codes in the suggested_command, description, and explanation fields. To make your life easier, we offer a helper class ```Colorize``` with the following methods:

 + **append** to add a message in the builder.
 + **emoji** to add a emoji code. You can use Colorize default codes for predefined ones.
 + **info** to change the text to info color.
 + **warning** to change the text to show warnings or errors.
 + **complete** to change the text to show completed actions or positive outcomes.
 + **normal** to come back to the normal color code.
 + **to_console** to get the text formatted and ready for printing and return the console to the original state.

See an example [here](search_agent/search_agent.py#L72).

## Interaction Patterns

We described some of the "interaction patterns" with the end user [here](../../../README.md). 
From the developer's perspective, the API lets them intercept as well as execute a callback on every user input 
on the command line *after the user hits return*, and lets them respond appropriately depending on what functionality their skill provides. You can thus use this API to:

+ Do nothing and let normal life on the command line follow.
This includes doing nothing but registering an event to
learn from that event and/or track user state.
+ Add something to the user input -- e.g. a flag that would make a command work.
+ Replace the user input by something else -- e.g. respond to a natural language request for automation.
+ Respond to the outcome (e.g. error) of a user command for in-situ support and troubleshooting.
+ Add something to the outcome -- e.g. for proactive support and/or pedagogical purposes.

The operation of the skill hinges on two methods: `get_next_action` and `post_execute`.

### Intercept an user command

The API intercepts any user input (e.g. a command in natural language or a regular Bash command)
using the `get_next_action(self, state: State) -> Action` method: it receives the State object 
from the terminal as the percept and returns an Action object to the terminal as the directive
on how to respond.

### Follow-up on execution of command

The API intercepts the `stdout`/`stderr` so that a skill can respond to the execution of a 
command on the terminal (and subsequent errors, if any) appropriately.
The `post_execute(self, state: State) -> Action:` method takes 
in the `State` object as before as the percept from the environment
(this time, after the execution of an action)
and again returns an `Action` object as the directive to the terminal on how to react.

> **Note:** As of now, you cannot execute another command in response to the execution,
but you can suggest a new one in the `description` field.
Thus the suggested command in post-execution is *always* NOOP.

These two features are feature complete in surfacing the above interaction patterns to the user.
Browse the provided skills in this directory to watch them come alive across a diverse set 
of AI capabilities in NLP, Planning, etc. 

## Debugging

To try out your skill on the bash, every time you make an update to it, you must reinstall the CLAI package again. 
For instructions on installing and uninstalling CLAI, see [here](../../../README.md). 
**Make sure to restart your shell every time you uninstall and install CLAI for your changes to take effect.**

> **Note:** If you encounter an error while testing your skill inside Bash, you can access the error in the python output by executing `>> cat nohup.out` from the location you invoked the CLAI-enabled bash. You may have to restart (or in the worst case, re-install) CLAI if the error has caused the CLAI server to crash. 

> **Note:** For more detailed logs do:

```
from clai.server.logger import current_logger as logger
logger.info("debug message")
```

See [here](ibmcloud/ibmcloud.py#L44) for an example. The logs can be found in `/var/tmp/app.log`.

### Integration Tests

Once you are happy with your skill, you can check in sample inputs and outputs in
[\<root\>/test_integration](../../../test_integration/) to make sure your skills runs as intended.
See [here](../../../test_integration/test_skill_nlc2cmd.py) for an example test with the `nlc2cmd` skill.
This simulates the user on a terminal inside a container 
and checks for the skill's intended input in the stdout/stderr.
Once all the tests have passed, and you are satisfied with the skill, open a PR to add your skill
to the CLAI catalog as per the instructions [here](../../../CONTRIBUTING.md).


## Saving and Loading Skills

The save and load functionionality allows agents to persist their state on disk which can then be loaded in a future iteration to continue the agent from a previously saved state. This can be used by stateful agents such as RL-based agents to learn and update their parameters during an interaction and save them when the session ends. In the next session, these agents can load the previously learned state and continue their learning for the next session.

1. `get_agent_state() -> dict` This function allows agent developers to define the state composition of an agent. This is saved on the disk for future recall. The state of an agent is defined as a dictionary with key being the variable identifier and the corresponding value being the variable itself.

2. `save_agent() -> bool` This function saves the state as defined in `get_agent_state` onto the disk. It returns `True` if the save is successful and `False` if there is an error. This function is, by default, called in the destructor of the `Agent` class to save the agents at the end of their lifecycle, but can also be called anytime by the developer.

3. `load_saved_state() -> dict` This function returns the last saved state for the agent. The returned state is in the same format as defined in the `get_agent_state` function. This function can be used by the agent to get the most recently saved state back and load it back into the agent parameters.

> **Note:** By default, the saved files are stored in `$HOME/.clai/saved_agents`. The base directory (by default `$HOME/.clai`) can be controlled by setting the `CLAI_BASEDIR` environment variable.

## The Orchestration API 

The orchestration layer rates, ranks and descides which skills to surface to the end user. 
You can implement your own selection method using the [`Orchestration API`.](../README.md)

----------

## Looking for inspiration? 

[`Terminals Are Sexy`](https://terminalsare.sexy/) 
[`Awesome Bash`](https://github.com/awesome-lists/awesome-bash) 
[`Bash it`](https://github.com/Bash-it/bash-it) 
[`Oh My Zsh`](https://github.com/robbyrussell/oh-my-zsh) 
[`Oh-My-Bash`](https://ohmybash.github.io/) 
[`The Fuck`](https://github.com/nvbn/thefuck) 
[`tldr`](https://github.com/tldr-pages/tldr) 
[`devhints.io`](https://devhints.io/bash) 

We are, of course, indebted and inspired by the open-source community around building plugins for the command line. In CLAI we have attempted to expand the scope of how developers can interface to the Bash (especially keeping the AI agent architecture in mind). A shout out to the above (non-exhaustive) list of plugins for the command line, if you are looking for some inspiration!  

We [:heart:](https://www.zdnet.com/article/good-news-for-developers-the-cli-is-back/) Bash.
