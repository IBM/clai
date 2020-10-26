# GPT-3 Utility

GPT-3 ([Brown et. al.](https://arxiv.org/abs/2005.14165)) is a large-scale (175 billion parameter) language model 
developed by [OpenAI](https://openai.com/), with impressive task-agnostic, few-shot performance. It has 
been applied to tasks including but not limited to natural language shell, code 
(regex, devops, sql) generation, text summarization, story writing, among others.
A curated list of application is available at [GPT3 Examples](https://gpt3examples.com/).

Since GPT-3 is a task-agnostic model, "priming" or initializing the model with a few labeled examples 
is important to make it work for a specific task. This utility serves as an interface to the GPT-3 REST based 
[API](https://openai.com/blog/openai-api/) along with providing a programmatic way to prime the model.


## Methods

- ### Example class

  - `def __init__(ip, op)`: represents a priming example for GPT-3 initialization with the input `ip` and output `op` pairs


- ### GPT class

  - `def __init__(**kwargs)`: initializes the GPT-3 API class with model specific parameters. These parameters include the 
  model engine, temperature, maximum number of tokens, priming syntax, among others, more details of which can be obtained 
  with the API documentation from OpenAI

  - `def set_api_key(self, key)`: sets the OpenAI API authentication key. Required for API call and can be obtained through 
  [link](https://openai.com/blog/openai-api/)

  - `def add_example(self, ex)`: adds a priming example to the class

  - `def delete_example(self, id)`: deletes a priming example identified by id

  - `def get_prime_text(self)`: returns the priming text used to initialize the model

  - `def submit_request(self, prompt)`: calls the GPT-3 REST API with the prompt and the priming examples 
  added to the class object. Returns the JSON response from the API.

  - `def get_top_reply(self, prompt, strip_output_prefix=False)`: calls the GPT-3 REST API with the prompt and the priming examples
  and returns the top reply from the model.


## Usage within plugins

- [`voice`](../../plugins/voice) (`text-summarization`) <br> `voice` plugin is a smart screen reader that utilizes
GPT-3 to summarize the shell error message to be read back to the user.


## Acknowledgement

We utilize code in the [GPT-3 sandbox](https://github.com/shreyashankar/gpt3-sandbox) repository 
for this utility, and would like to acknowledge and thank the repository contributors for the 
appropriate sections of the code
