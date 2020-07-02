## Metric computation

This module provides the metric computation used by the nlc2cmd command as a python package 
that participants can use to import in their code for experimentation.


### Installation:
```
pip install -r requirements.txt
```


### Computing metric in a python shell:

```python
from metric import  metric_utils

ground_truth = 'find . -name "*.txt" -print | less'
predicted_cmd = 'find . -name "*.txt" -print'
predicted_confidence = 1.0

metric_val = metric_utils.compute_metric(predicted_cmd, predicted_confidence, ground_truth)
# metric_val would be 0.5 in this case
```