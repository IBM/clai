# howdoi

`NLP` &nbsp; `Q&A` &nbsp; `Retrieval` &nbsp; `Support`

This skill is used to do a natural language search over a corpus to recommend a command based on the user's question. 
Currently, it uses the [Stack Exchange Unix forum](https://unix.stackexchange.com/) as the corpus for the search. 

## Implementation

The skill is composed of:
1. A REST API deployed on [IBM Cloud](https://cloud.ibm.com/) that responds to the user query; and 
2. Local code for the skill using the CLAI API that decides when to call the REST API and how to then serve the response back to the CLAI-enabled terminal.

The user query is searched against the Stack Exchange Unix forum to find 
an accepted answer, or the most highly rated answer in case an accepted answer is unavailable. 
As an illustration, we have employed a simple index-based [text search](https://docs.mongodb.com/manual/text-search/) 
that comes built-in with MongoDB. 
The body of that answer is then compared against available manpages using a REST API from 
[man page explorer](../manpage_agent/) 
to recommend a relevant command to explore. 

[`Download corpus data`](https://archive.org/download/stackexchange/unix.stackexchange.com.7z)

Note that this is merely illustrative of the "how do i" interaction pattern on the CLAI-enabled command line
and the accuracy of the recommendations is highly dependent on the quality of the implemented search on the 
Stack Exchange Unix forum data as well as the answer quality of the matched question. 
We hope to build, as a community, standards and benchmarks to make this more accurate over time.
Watch this space!

## Example Usage

![howdoi](https://www.dropbox.com/s/x0iclad93s7pacf/howdoi.gif?raw=1)

The skill will respond to how/what questions if it finds a reasonable solution. Try out:

1. `when to use sudo vs su?`
2. `find out disk usage per user?`
3. `how to process gz files?`

## [xkcd](https://uni.xkcd.com/)
Sadly, this is a true story.  At least I learned about the OS X 'say' command.

![alt text](https://imgs.xkcd.com/comics/im_an_idiot.png "Sadly, this is a true story.  At least I learned about the OS X 'say' command.")
