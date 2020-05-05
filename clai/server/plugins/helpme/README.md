# helpme

`NLP` &nbsp; `Retrieval` &nbsp; `Support`

This skill is used to recommend relevant results from one or more
[search providers](../../searchlib/) whenever you encounter an error on the
command line. This is intended to allow you to remain in context and continue
working on the terminal without having to leave your development environment and
go searching for a solution on the Internet.

## Implementation
The skill is composed of:
1. One or more search providers that respond to an error message on the command
line user query; and 
2. Local code for the skill using the CLAI API that decides when to call the
REST API and how to then serve the response back to the CLAI-enabled terminal.

The `helpme` skill is always on alert to assist you in your time of struggle. It
actively monitors standard error logs and when an error occurs, it queries
each search provider in the order in which they are defined in the `config.ini`
configuration file. The body of the first result found is then compared against
available manpages using a REST API from [man page explorer](../manpage_agent/)
to recommend a relevant command to explore. 

[`Download corpus data`](https://archive.org/download/stackexchange/unix.stackexchange.com.7z)

Note that this is merely illustrative of the "help me" interaction pattern on
the CLAI-enabled command line and the accuracy of the recommendations is highly
dependent on the quality of the implemented search on the search provider data
as well as the answer quality of the matched question. For now, the confidence
is [boosted artificially](Lx) to illustrate this interaction pattern. We hope to
build, as a community, standards and benchmarks to make this more accurate over
time. Watch this space!

## Example Usage

![helpme](https://www.dropbox.com/s/molqz37ll2kbraa/helpme.gif?raw=1)

The skill will respond on `stderr` if it finds a reasonable solution.

## Future Design Enhancements
While multiple search providers are supported by `helpme`, it simply returns the
first result encountered.  A better way forward would be for `helpme` to query
_all_ search providers, collate their results, rank them, and return the result
with the highest ranking.  It could then prompt the user if they are happy with
this result; if they are not, `helpme` could return the next highest-ranked
result.

## Original Design
The original design of `helpme` supported only the Stack Exchange Unix forum.
The user query was searched against the Stack Exchange Unix forum data to find 
an accepted answer that solves the issue, or a most highly rated answer in case
of accepted answer being unavailable.  Similar to the [howdoi](../howdoi/)
skill, it employed a simple index-based
[text search](https://docs.mongodb.com/manual/text-search/) to identify the
relevant Stack Exchange post and the corresponding answer.

## [xkcd](https://uni.xkcd.com/)
All long help threads should have a sticky globally-editable post at the top
saying 'DEAR PEOPLE FROM THE FUTURE: Here's what we've figured out so far ... 

![alt text](https://imgs.xkcd.com/comics/wisdom_of_the_ancients.png "All long help threads should have a sticky globally-editable post at the top saying 'DEAR PEOPLE FROM THE FUTURE: Here's what we've figured out so far ...")
