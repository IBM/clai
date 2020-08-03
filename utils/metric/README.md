## Metric computation

This module provides the metric computation used by the nlc2cmd command as a python package 
that participants can use to import in their code for experimentation.

:arrow_down: Get the code by either cloning this repo or through the link: [https://ibm.box.com/v/metric-computation-code](https://ibm.box.com/v/metric-computation-code)


### Installation:
```
pip install -r requirements.txt
```


### Computing metric in a python shell:

```python
from metric import  metric_utils

ground_truth = 'find . -type f -ctime -3 | tail -n 5'
predicted_cmd = 'find . -type f | tail -n 5'
predicted_confidence = 1.0

metric_val = metric_utils.compute_metric(predicted_cmd, predicted_confidence, ground_truth)
# metric_val would be 0.75 in this case
```

### Other examples

```
-----------------------------------------------------------------------------------------
1. Parameters are not taken into consideration

    >> ground_truth = df | grep /dev/disk0s2
    >> predicted_cmd = df | grep diskpath
    >> predicted_confidence = 1.0

    >> metric_val = 1.0
-----------------------------------------------------------------------------------------

2. Order of flags does not matter

    >> ground_truth = find . -regextype posix-egrep -regex '^.*/[a-z][^/]*$' -type f
    >> predicted_cmd = find . -type f -regextype posix-egrep -regex '^.*/[a-z][^/]*$' 
    >> predicted_confidence = 1.0

    >> metric_val = 1.0
-----------------------------------------------------------------------------------------

3. You get negative points if you translate to the wrong utility

    >> ground_truth = mkdir directory
    >> predicted_cmd =  touch directory
    >> predicted_confidence = 1.0

    >> metric_val = -1.0
-----------------------------------------------------------------------------------------

4. Order of utilities matter

    >> ground_truth = df --total | tail -n 1
    >> predicted_cmd =  tail -n 1 | df --total
    >> predicted_confidence = 1.0

    >> metric_val = -1.0
-----------------------------------------------------------------------------------------

5. Predicting excessive flags gets negative penalty

    >> ground_truth = find / -name linux
    >> predicted_cmd =  find / -EXdsx -name linux
    >> predicted_confidence = 1.0

    >> metric_val = 0.1666
-----------------------------------------------------------------------------------------
```
