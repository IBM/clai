# Man Pages dataset

Download link: [https://ibm.box.com/v/nlc2cmd-manpagedata](https://ibm.box.com/v/nlc2cmd-manpagedata)


The Man Pages dataset contains a JSON structured text of the man pages of commands available in 
Ubuntu's 18.04 LTS distribution. It contains the information for over 36000 commands defined 
[here](http://manpages.ubuntu.com/manpages/bionic/), and each commands man page is parsed using the 
[explainshell](https://github.com/idank/explainshell) parser.


### Data structure

Owing to the size of the dataset, the entire data file does not contain a valid JSON string. Instead,
each line in the file defines the parsed data for one command and is a valid json string. This allows
easy iterative loading of the dataset without overflowing the memory.

The structure of each JSON string is as follows:

```
{
    "_id": {"$oid": str}, 
    "source": str,
    "name": str,            
    "synopsis": str,         
    "paragraphs": [         
        ...
        {
            "idx": int, 
            "text": str, 
            "section": str, 
            "is_option": bool,          // does the paragraph define an option
            "short": [str],             // short option name (ex: -h, -r)
            "long": [str],              // long option name (ex: --help, --root-uri)
            "expectsarg": bool,         // does the option expect an argument or not
            "argument": None, 
            "nestedcommand": bool
        },
        ... 
    ], 
    "partialmatch": bool, 
    "multicommand": bool, 
    "updated": bool, 
    "nestedcommand": bool,
    "aliases": [[str, int]]
}

```


### How to load the dataset

You can use the following code to iteratively load the dataset using Python

```python
f = open(filepath, "r")
for line in f:
    cmd_manpage = json.loads(line)
```