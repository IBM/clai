# helpme

`NLP` &nbsp; `Retrieval` &nbsp; `Support`

This skill is used to recommend relevant results from a platform-appropriate
[search provider](../../searchlib/) whenever you encounter an error on the
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
the appropriate search provider for your platform. The body of the result is
then compared against available manpages using a REST API from
[man page explorer](../manpage_agent/) to recommend a relevant command to
explore. 

## Search Providers
### Stack Exchange Unix Forums
For users running on Linux or OSX, their query is searched against the Stack
Exchange Unix forum data to find an accepted answer that solves the issue, or a
most highly rated answer in case of an accepted answer being unavailable.
Similar to the [howdoi](../howdoi/) skill, this employs a simple index-based
[text search](https://docs.mongodb.com/manual/text-search/) to identify the
relevant Stack Exchange post and the corresponding answer.

[`Download corpus data`](https://archive.org/download/stackexchange/unix.stackexchange.com.7z)

Note that this is merely illustrative of the "help me" interaction pattern on
the CLAI-enabled command line and the accuracy of the recommendations is highly
dependent on the quality of the implemented search on the search provider data
as well as the answer quality of the matched question. For now, the confidence
is [boosted artificially](Lx) to illustrate this interaction pattern. We hope to
build, as a community, standards and benchmarks to make this more accurate over
time. Watch this space!

### IBM KnowledgeCenter
For users running on z/OS, their query is searched against the IBM
KnowledgeCenter databases for the z/OS 2.4 product, with the tag for Unix
System Services ("USS") applied. `helpme`searches the corpus of IBM
publications, then Redbooks, then DeveloperWorks articles, and then finally
Technotes. Unlike the Unix Stack Exchange search provider, this is very
simplistic; the first result found in any KnowledgeCenter database query is the
result returned to the user.

## Example Usage

![helpme](https://www.dropbox.com/s/molqz37ll2kbraa/helpme.gif?raw=1)

The skill will respond on `stderr` if it finds a reasonable solution.

## Future Work
Today, `helpme` visits each search provider in the order they were defined in
the `config.ini` configuration file,and uses the first result encountered
as the basis for what it returns to the user.  The configuration file defines
three search providers: the Stack Exchange Unix forums, the IBM KnowledgeCenter,
and the man page explorer.  The man page explorer is treated as a special case,
Stack Exchange is only enabled on Linux and OSX, and the IBM KnowledgeCenter is
only enabled on z/OS.  As a result, the net effect is that on Linux/OSX `helpme`
queries only the Stack Exchange forums, and on z/OS `helpme` only queries the
IBM KnowledgeCenter.

A better way forward would be for `helpme` to query _all_ search providers,
collate their results, rank them, and return the result with the highest
ranking. It could then prompt the user if they are happy with this result; if
not, `helpme` could return the next highest-ranked result.

## [xkcd](https://uni.xkcd.com/)
All long help threads should have a sticky globally-editable post at the top
saying 'DEAR PEOPLE FROM THE FUTURE: Here's what we've figured out so far ... 

![alt text](https://imgs.xkcd.com/comics/wisdom_of_the_ancients.png "All long help threads should have a sticky globally-editable post at the top saying 'DEAR PEOPLE FROM THE FUTURE: Here's what we've figured out so far ...")
