## Preference-based Orchestration

The `preference_orchestrator` picks the skill with highest confidence above a threshold that do not violate any of the partial (ordering) preferences specified. It pools all the skills whose confidences are above the specified threshold and then goes down the list in decreasing order of confidence, selecting the first one that does not break any of the ordering constraints.

+ The [config.json](./config.json) file allows you to specify the threshold and a set of partial preferences
+ Each preference `[x,y]` is evaluated in order and reads as `x is preferred to y` -- the skill with the highest confidence that 
does not violate any of these orders is selected for execution.
