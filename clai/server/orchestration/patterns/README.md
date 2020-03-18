## Orchestration Patterns

This directory contains some sample orchestration patterns. The [`max_orchestrator`](./max_orchestrator/) is used by default, 
as specified in [configPlugins.json](../../../../configPlugins.json). Use the [`Orchestration API`](../../) to make your own orchestration patterns. 

+ **`max_orchestrator`** picks the skills that responds with the highest confidence, above a certain threshold. 
+ **`preference_orchestrator`** picks the skill with highest confidence above a threshold that do not violate any of the partial preferences specified by the user. 
+ **`threshold_orchestrator`** is similar to the max_orchestrator but it maintains thresholds for confidences specific to each skill  and updates them according to how the end user reacts to them.
+ **`bandit_orchestrator`** learns user preferences using contextual bandits.
