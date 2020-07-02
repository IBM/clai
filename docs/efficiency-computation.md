# Energy consumption computation

Besides measuring the accuracy of the predicted command for the nl2cmd competition, we also focus 
on the energy consumption of the model. This should inspire participants to also consider the 
energy requirements of their models along with the accuracy metric, and possibly create more energy
efficient models.

We use the [energyusage](https://github.com/responsibleproblemsolving/energy-usage) library to compute
the energy usage of the method. The energy consumption computed is the average energy (kWh) used by 
the predict method for each invocation.


### Note

- The energyusage library is available only for Linux Kernels that have the RAPL interface. 
See [energyusage limitations](https://github.com/responsibleproblemsolving/energy-usage#limitations).
Owing to this, while testing your submission locally, depending on your system configuration, the
library might not work. In these circumstances, the energy usage is returned as 0.0 kWh. However,
while evaluating your submission on our end, we'll ensure that energyusage library is supported and run.