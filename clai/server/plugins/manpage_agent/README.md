# man page explorer

`Q&A` &nbsp; `NLP` &nbsp; `Retrieval`

This skill allows you to ask Bash for relevant commands by describing your task in natural language. The command whose man page document matches most with the users query is suggested by the skill.

## Implementation

The skills is structured as a REST API deployed on [IBM Cloud](https://cloud.ibm.com/) responding to the users query, and a local agent deciding when to call this REST API, and then serving the API response back to CLAI.

The REST API is housed in the [`webapp`](./webapp) folder. The [`train_sklearn_agent.sh`](./webapp/train_sklearn_agent.sh) file fetches all the man pages in the system, and then trains a sklearn TF-IDF vectorizer on the collected corpus. All the man pages are then encoded using this trained vectorizer. The [`app.py`](./webapp/app.py) file loads the saved sklearn TF-IDF vectorizer model, and on receiving a query, encodes it using the same vectorizer, and returns the command whose man page has the highest cosine similarity with the encoded query.

On the local system, the skill decides to call the API if the query is detected as a question [[`code`]](./question_detection.py), gets the suggested command from the API, and also integrates the [`tldr`](https://tldr.sh/) plugin to summarize the suggested command. 

## Example Usage

![manpage-agent](https://www.dropbox.com/s/7so8yumbaip7b0o/man%20page%20agent.gif?raw=1)

1. `>> how to clear screen`
2. `>> how do I change the file owner`
3. `>> how to compile java class file`
4. `>> how to compress a file into a tar file?`

## [xkcd](https://uni.xkcd.com/)
Life is too short for man pages, but occasionally much too short without them.

![alt text](https://imgs.xkcd.com/comics/rtfm.png "Life is too short for man pages, but occasionally much too short without them.")
