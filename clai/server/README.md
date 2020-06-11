# The Orchestration Layer
This layer orchestrates how different skills can are rated, ranked and surfaced to the end user. 
Before learning about Orchestration, please read about CLAI [interaction patterns](../../README.md) 
and [skills](plugins/README.md) first.
The orchestration layer comes with its unique set of challenges. 
In general, there are at least two orchestration methods: 

+ **apriori** where the orchestrator acts as a filter and decides which skill to invoke based on the input; and 
+ **posterior** where all the skills listen and respond, and let the orchestrator pick the best response.

The apriori option is likely to have a significantly smaller system footprint, but
involves a single bottleneck based on the accuracy of the classifier which determines which plugin to invoke. 
Furthermore, this requires that the orchestrator design be cognizant of the list of plugins and their capbilities 
-- this is unrealistic.  

The posterior option -- despite increased latency and computational load -- keeps the skill design process independent from the orchestration layer *as long as the confidences are well calibrated*.
This can be achieved by learning from user responses to CLAI actions, 
and gradually adapting a normalizer or a more sophisticated selection strategy 
over the confidences self-reported by the skills. 
The ability to learn such patterns can also be used to eventually realize a healthy mix of apriori 
and posterior orchestration strategies. 

## Sample Orchestrators

CLAI comes with a set of orchestrators to help you get the best out of the Orchestration API.

> [`max_orchestrator`](orchestration/patterns/max_orchestrator) This picks the skills that responds with the highest confidence, above a certain threshold. This is the default choice as specified [here](../../configPlugins.json).

> [`preference_orchestrator`](orchestration/patterns/preference_orchestrator) picks the skill with highest confidence above a threshold that do not violate any of the partial (ordering) preferences specified by the user.

> [`threshold_orchestrator`](orchestration/patterns/threshold_orchestrator) This is similar to the `max_orchestrator` but it maintains thresholds specific to each skill, and updates them according to how the end user reacts to them.

> [`bandit_orchestrator`](orchestration/patterns/rltk_bandit_orchestrator) This learns user preferences using contextual bandits. 

These are housed in the [orchestration/patterns/](orchestration/patterns) folder under packages with the same name. Follow them as examples to build your own favorite orchestration pattern. 

## The Orchestrator API 

### Anatomy of an Orchestrator

Every orchestrator you want to make available to CLAI is housed in this directory.

```
<root>
- clai
  + tools
  + emulator
  ...
  - server
    + command_runner
    ...
    - orchestration
      - patterns
        - pattern_1
          - manifest.properties
          - install.sh
          - pattern_1.py
        + pattern_2
        + pattern_3
        ...
+ docs
+ bin
+ scripts
...
```

### The Manifest 

A `manifest.propertie`s file which documents the name, a brief description, and the default installation status of the orchestration pattern. Here is an [example](./orchestration/patterns/max_orchestrator/manifest.properties).

```
[DEFAULT]
name=dummy pattern
description=This is a dummy pattern
exclude=true
```

+ **name:** This is the name your orchestration pattern.
+ **description:** This is a text description of your pattern (supports ASCII) that appears when you list all the patterns on the command line in verbose form. 
+ **exclude:** This is a boolean flag (see above) that you can use to tell CLAI not to list a pattern among those available to the user on the command line. For example, the `bandit_orchestrator` uses an IBM internal package and is hence not listed. 

At runtime, you can list available orchestrators like so:

```
>> clai orchestrate 
Available Orchestrators:
☑ max_orchestrator
◻ preference_orchestrator
◻ threshold_orchestrator
```

You can use the `-v` flag to print out the desriptions in the manifest. You can also switch between orchestration patterns using the orchestrate command. 

```
>> clai orchestrate preference_orchestrator
Available Orchestrators:
◻ max_orchestrator
☑ preference_orchestrator
◻ threshold_orchestrator
```

### The Installer

An `install.sh` file that installs all dependencies required by the orchestrator. 
All the orchestrators are installed at the time of installation of CLAI.
Here is an [example](./orchestration/patterns/max_orchestrator/install.sh).

## The Code

Finally the main python file that houses your skill should match the folder name (here is an [example](./orchestration/patterns/max_orchestrator/max_orchestrator.py)). The class name for your skill can be any name as long as it inherits the `Orchestrator` class. 

The Orchestrator API implements a posterior orchestration layer for CLAI: 

+ Any time an user hits return on the terminal, the command is broadcasted to all the active skills . 
The skills respond with self-determined confidences,
and the Orchestrator picks among them according to some criterion. 
This allows the skills to, for example, intercept a natural language command or question.

+ The same process repeats once the action is executed and the output on the terminal is again broadcasted 
to all the active skills, which again respond with their respective confidences.
This allows the skills to, for example, suggest a fix to an error on the terminal.

Let us examine this flow of control through the Orchestration Layer in detail first. 
Consider the following example:

```
>> clean <-- previous command
clai :: do you mean clear? (y/n/e) n <-- pre-process
command not found <-- stdout/stderr
clai :: maybe try out clear instead <-- post-process
>> clear <-- current command
```

As we described before, the Orchestrator is invoked twice: once in the **pre-processing** stage when the user has just typed in a command -- this is then broadcasted to all the active skills each of which respond with a self-determined confidence -- and again in the **post-processing** stage when a command has been executed on the shell and the stdout/stderr is again piped through all the active skills. In each of these two stages, the task of the Orchestrator is to **Choose** from among the skills that responded, which one to pass onto the end user.

### Choose

+ `choose_action` This method is the key in the implementation of the Orchestrator. 
It decides how a skill is selected form an array of responses from the active skills.
The method receives the following inputs (and returns an:

| parameters | type | comment |
|------------|------|-------------|
| command | State | State object representing system state. |
| candidate_actions | list | List of candidate Action objects. |
| agent_names | list | List of active skills that responded with candidate Actions. |
| force_response | bool | Whether CLAI has been forced to respond (refer to [Interaction Patterns](../../README.md)). |
| pre_post_state | str | `pre` pr `post` depending on the stage of execution. |

It returns the following tuple `(selected_candidate, agent_name)`:

| parameters | type | comment |
|------------|------|-------------|
| selected_candidate | Action | This is the Action object returned as directive to the terminal. |
| agent_name | str | This is the name of the skill that is selected. |

> **Note:** The `State` and `Action` objects are described in detail [here](plugins/README.md). 

The **Choose** functionality is enough for a static Orchestrator like the `max_orchestrator` as shown [here](orchestration/patterns/max_orchestrator/max_orchestrator.py#L30).
However, more sophisticated selection strategies can be *learned* based on how the user reacts at
the pre- and post-processing stages. The **Observe** functionality allows the developer access to the user feedback.

### Observe 

+ `record_transition` This method is also invoked in the pre-processing stage. It provides access to the history of the last interaction on the shell and thus provides an opportunity for the Orchestrator to learn from the user interactions. For example, you can use this to determine if a suggested command taken up by the user either directly (by responding `y` to it) or indirectly (by executing a command contained in the suggestion either during the pre- or the post-execution process.
The method receives the following inputs (it does not return anything).

| parameters | type | comment |
|------------|------|-------------|
| prev_state_pre | TerminalReplayMemory | This is at the pre-process stage of the previous command. |
| prev_state_post | TerminalReplayMemory | This is at the post-process stage of the previous command. |
| current_state_pre | TerminalReplayMemory | This is at the pre-process stage of the current command. |

A `TerminalReplayMemory` object has the following fields:

| parameters | type | comment |
|------------|------|-------------|
| command | State | State object representing system state. |
| force_response | bool | Whether CLAI has been forced to respond (refer to [Interaction Patterns](../../README.md)). |
| candidate_actions | list | List of candidate Action objects. |
| agent_names | list | List of active skills that responded with candidate Actions. |
| suggested_command | Action | Action object representing actionable directive to the terminal. |
| suggested_agent_name | str | Name of the skill that got selected. |

Going back to the example above:

```
prev_state_pre.command.suggested_command = clear
prev_state_post.command.suggested_command = None 
prev_state_post.command.description = maybe try out clear instead 
current_state_pre.command.suggested_command = clear
```

> **Note:** The post-processing step always has `None` as the suggested command since the architecture currently does not support executing another action in response to an executed command. Until this changes, the response is thus always to be found in the `description` field.

> **Note:** The feedback of whether an user used a suggested action from the pre-processed step is in `prev_state_post.command.suggested_executed` and **not** in `prev_state_pre.command.suggested_executed`.

> **Note:** The feedback is recorded in the next action since once way want to look at the follow-up to see whether the user is using a suggestion, i.e. the feedback may not always be directly tied to the user response on `y/n/e` during the current pre-process stage. This is especially the case when skills -- such as the [`nlc2cmd skill`](plugins/nlc2cmd) -- do not suggest a command that can be used directly. 

Check out the `bandit_orchestrator` for an [example](orchestration/patterns/rltk_bandit_orchestrator/rltk_bandit_orchestrator.py). 

### Save and Load

An Orchestrator instance is destroyed once a terminal session ends. 
Thus, to ensure that a learned selection strategy persists across multiple sessions, 
the Orchestrator API implements load and save methods with an internal state representation, 
identical to the [save and load functionality of skills](plugins/README.md). 

1. `get_orchestrator_state() -> dict` This function allows developers to define the state of an Orchestrator. This is saved on the disk for future recall. The state is defined as a dictionary with key being the variable identifier and the corresponding value being the variable.

2. `save() -> bool` This saves the state as defined in `get_orchestrator_state` onto the disk. It returns True if the save is successful and False otherwise. This function is, by default, called in the destructor of the Orchestrator class to save the agents at the end of their lifecycle, i.e. when a terminal session end, but it can also be called anytime by the developer.

> **Note:** By default, the saved files are stored in `$HOME/.clai/saved_orchestrators`.  The base directory (by default `$HOME/.clai`) can be controlled by setting the `CLAI_BASEDIR` environment variable.

3. `load() -> dict` This function returns the last saved state for the Orchestrator. The returned state is in the same format as defined in the `get_orchestrator_state` function. This function can be used by the agent to get the most recently saved state back and load it back into the Orchestrator parameters.

Check out the `threshold_orchestrator` for an example of [maintaining state](orchestration/patterns/threshold_orchestrator/threshold_orchestrator.py#L19) and [loading from a saved state](orchestration/patterns/threshold_orchestrator/threshold_orchestrator.py#L26). 

## Related Publications and Links

> A Bandit Approach to Posterior Dialog Orchestration Under a Budget. 
Sohini Upadhyay, Mayank Agarwal, Djallel Bounneffouf, Yasaman Khazaeni.
NeurIPS 2018 Conversational AI Workshop.

> A Unified Conversational Assistant Framework for Business Process Automation. 
Yara Rizk, Abhisekh Bhandwalder, Scott Boag, Tathagata Chakraborti, Vatche Isahagian, Yasaman Khazaeni, 
Falk Pollock, and Merve Unuvar. AAAI 2020 Workshop on Intelligent Process Automation. 
