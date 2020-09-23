# searchlib

`NLP` &nbsp; `Retrieval` &nbsp; `Support`

Library for managing _search providers_, RESTable interfaces on which a client
routine can perform search queries.

## What makes a "search provider"?
As far as `searchlib` is concerned, a search provider is a RESTable interface
that we can send a search query to and receive a response containing a list of
results.  Client code will interface with search providers through a set of
standardized interfaces, outlined in this document.  At the implementation
level, each search provider must be defined in this library so that the
standardized interfaces map to the provider's implementation-specific RESTable
API.

## Standardized interface
The standardized external interface is defined through two classes:
 * `data.py:Datastore`
   * Defines the primary external interface for search providers
   * Methods:
     * `get_apis(self) -> OrderedDict`
       * Returns an `OrderedDict` of APIs, where each member is stored in the
         order it was encountered in the configuration file
       * The dictionary key values are the search providers' names and are of
         type `str`
       * The dictionary members are subclasses of `providers.py:Provider`
     * `search(self, query, service='stack_exchange', size=10, **kwargs) -> List[Dict]`
       * Ask the search provider named `service` to search on the string
         `query` using the implementation-specific parameters in `kwargs` and
         returning at most `size` results
  * `providers.py:Provider`
    * Superclass for all search providers
    * Methods:
      * `can_run_on_this_os(self) -> bool`
        * Returns `True` if this search provider can be used on the client OS
      * `get_excludes(self) -> list`
        * Returns a list of operating systems that the search provider cannot
          be run from
      * `has_variants(self) -> bool`
        * Returns `True` if this search provider has more than one search
          variant
      * `get_variants(self) -> list`
        * Returns a list of search variants supported by this search provider
    * All search providers must implement the following abstract methods:
      * `call(self, query:str, limit:int = 1, **kwargs)`
        * Perform a query on the string `query` using the
         implementation-specific parameters in `kwargs` and returning at most
         `limit` results
      * `extract_search_result(self, data:List[Dict]) -> str`
        * Extract the result string from the data returned by an API search
      * `get_printable_output(self, data:List[Dict]) -> str`
        * Return an informative string that can be displayed to the user

## Configuration
Each section in the skill's `config.ini` file denotes a specific search
provider, with one required and three optional parameters per section:

 * `api` URL for the RESTful search provider. (Required)

 * `variants` A space-separated list of _search variants_, as some search
   providers provide support for different database searches.  The order in
   which the variants are listed here is the order in which they will be
   searched. If no `variants` line is supplied, the search provider will use its
   default search database.

    * For example: the IBM KnowledgeCenter uses a collection of IBM
      publications as its default search database, but also contains
      databases for searching DeveloperWorks, Redbooks, Technotes, and others.

 * `exclude` A space-separated list of client operating systems for which the search
      provider is ignored.  For example: a search provider containing the
      line `exclude=Linux Darwin` will be ignored when the CLAI client is Linux
      or MacOSX.

      * Valid exclude values are `Linux`, `Darwin`, `OS/390`, and `Z/OS`.

## Using search providers
In the root directory for your new skill, you should include a configuration
file.  This can have any name, but by convention it should be `config.ini`.
The layout of this configuration file should be as is
[described above](#configuration).

Example `config.ini`:

    # Provider: IBM KnowledgeCenter
    # Variants: Developerworks [Documentation] Redbooks Technotes
    [ibm_kc]
    api=https://www.ibm.com/support/knowledgecenter/v1/search
    exclude=Linux Darwin
    variants=Documentation Redbooks Developerworks Technotes
    
    # Provider: Unix StackExchange forums
    # Variants: None
    [stack_exchange]
    api=https://clai-stack-exchange-server.mybluemix.net/query
    exclude=OS/390 Z/OS
    
    # Provider: Manpages
    # Variants: None
    [manpages]
    api=https://clai-manpage-agent.mybluemix.net/findManPage/

Client code should import the `Datastore` object from `data.py`:

    from clai.server.searchlib.data import Datastore

To instantiate a new Datastore, pass the path to your skill's `config.ini` file
to the constructor during skill initiation:

    class MyAgent(Agent):
    def __init__(self):
        super(MyAgent, self).__init__()
        inifile_path = os.path.join(str(Path(__file__).parent.absolute()), 'config.ini')
        self.store = Datastore(inifile_path)

Iterating through providers:

    apis:OrderedDict=self.store.get_apis()
        for provider in apis:
            if provider == "manpages":
                print("We've found the Manpages provider!")

Querying the `stack-exchange` search provider and extracting its first result:

    thisAPI = apis["stack-exchange"]
    data = self.store.search(state.stderr, service="stack-exchange", size=1)
    if data:
        output:str = "Found the following result from the {}:\n{}" \
            .format(str(thisAPI), thisAPI.extract_search_result(data))
