## Remote router 

This flask application is a router for requests to our instance of the OpenAI API
that processes [NLC2CMD](http://ibm.biz/nlc2cmd) use cases. 
Note that we add the same prompt from the OpenAI example [here under "Speech to Bash" in the Demos](https://beta.openai.com/?demo=5) 
to the user command to seed the query. 

To bring up the server:

1. Fill in your [OpenAI API](https://openai.com/blog/openai-api/) access key in a file named `key`. 
You can apply for access [here](https://forms.office.com/Pages/ResponsePage.aspx?id=VsqMpNrmTkioFJyEllK8s0v5E5gdyQhOuZCXNuMR8i1UQjFWVTVUVEpGNkg3U1FNRDVVRFg3U0w4Vi4u).
2. Run `>> python3 run.py`

