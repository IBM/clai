# helpme

`NLP` &nbsp; `Retrieval` &nbsp; `Support`

This skill is used to recommend a relevant post from the [Stack Exchange Unix forum](https://unix.stackexchange.com/)
whenever you encounter an error on the command line.
This is intended to allow you to remain in context and continue working on the terminal without
having to leave your development environment and go searching for a solution on the internet.

## Implementation

The skill is composed of:
1. A REST API deployed on [IBM Cloud](https://cloud.ibm.com/) that responds to an error message on the command line user query; and 
2. Local code for the skill using the CLAI API that decides when to call the REST API and how to then serve the response back to the CLAI-enabled terminal.

The user query is searched against the Stack Exchange Unix forum to find 
an accepted answer, or the most highly rated answer in case an accepted answer is unavailable. 
As an illustration, we have employed a simple index-based [text search](https://docs.mongodb.com/manual/text-search/) 
that comes built-in with MongoDB. 
The body of that answer is then compared against available manpages using a REST API from 
[man page explorer](../manpage_agent/) 
to recommend a relevant command to explore. 

The `helpme` skill is always on alert to assist you in your time of struggle. It actively monitors standard error logs 
and when an error occurs, it searches against the Stack Exchange Unix forum data to find 
an accepted answer that solves the issue, or a most highly rated answer in case of accepted answer being unavailable. 
Similar to the [howdoi](../howdoi/) skill, we have employed a simple 
index-based [text search](https://docs.mongodb.com/manual/text-search/) 
to identify relevant stack exchange post and the corresponding answer. 

[`Download corpus data`](https://archive.org/download/stackexchange/unix.stackexchange.com.7z)

Note that this is merely illustrative of the "help me" interaction pattern on the CLAI-enabled command line
and the accuracy of the recommendations is highly dependent on the quality of the implemented search on the 
Stack Exchange Unix forum data as well as the answer quality of the matched question. 
We hope to build, as a community, standards and benchmarks to make this more accurate over time.
Watch this space!

## Example Usage

![helpme](https://www.dropbox.com/s/molqz37ll2kbraa/helpme.gif?raw=1)

The skill will respond on `stderr` if it finds a reasonable solution.

## [xkcd](https://uni.xkcd.com/)
All long help threads should have a sticky globally-editable post at the top saying 'DEAR PEOPLE FROM THE FUTURE: Here's what we've figured out so far ...  

![alt text](https://imgs.xkcd.com/comics/wisdom_of_the_ancients.png "All long help threads should have a sticky globally-editable post at the top saying 'DEAR PEOPLE FROM THE FUTURE: Here's what we've figured out so far ...")
