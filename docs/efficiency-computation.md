# Energy consumption computation

Besides measuring the accuracy of the predicted command for the nl2cmd competition, we also focus 
on the energy consumption of the model. This should inspire participants to also consider the 
energy requirements of their models along with the accuracy metric, and possibly create more energy
efficient models.

We use the [`experiment-impact-tracker`](https://github.com/Breakend/experiment-impact-tracker) library to compute
the energy usage of the method. The energy consumption computed is the power drawn (mW) by the `predict` function
for 100 invocations.
