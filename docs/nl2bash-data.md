# NL2Bash Data

Download link: [https://ibm.box.com/v/nl2bash-data](https://ibm.box.com/v/nl2bash-data)

The `NL2Bash` data contains over `12,000` instances of linux shell commands and their 
corresponding natural language descriptions provided by experts, from the 
[`Tellina`](https://github.com/TellinaTool/nl2bash/tree/master/data) system. 
The dataset features `100+` commonly used shell utilities.

### Data structure

The `nlc2cmd @ NeurIPS 2020` team has cast the `NL2Bash` data into a json format for ease of 
use, as follows:

```
{
	"id"(str): {
		"invocation": str,
		"cmd": str
	}
	
	...
}
```

The `invocation` field provides the natural language description, and the `cmd` field 
provides the corresponding command, which is a combination of the utility and the 
relevant flags and parameters.



### How to load the dataset

You can use the following code to load the dataset using Python

```python
import json

with open(filepath, 'r') as f:
    data = json.load(f)


print('Invocation: {} \nCommand: {}'.format(data['1']['invocation'], data['1']['cmd']))

# Output should be
# Invocation: Copy loadable kernel module "mymodule.ko" to the drivers in modules directory matchig current kernel. 
# Command: sudo cp mymodule.ko /lib/modules/$(uname -r)/kernel/drivers/

```
