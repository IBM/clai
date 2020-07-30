#!/usr/bin/env python3

'''
imports
'''
from flask import Flask, request
from flask_cors import CORS, cross_origin

import openai
import json
import os

'''
globals
'''

openai.api_key = open('key', 'r').read()
_cached_prompt = """Input: List files
Output: ls -l
Input: Count files in a directory
Output: ls -l | wc -l
Input: Disk space used by home directory
Output: du ~
Input: Replace foo with bar in all .py files
Output: sed -i .bak -- 's/foo/bar/g' *.py
Input: Delete the models subdirectory
Output: rm -rf ./models
Input: {}
Output:"""


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

'''
route: landing page
'''
@app.route("/")
def hello():
    return "Welcome to the router for the OpenAI API for the gpt3 skill in CLAI."

'''
route: gpt3 endpoint
'''
@app.route("/gpt3", methods=['GET', 'POST', 'PUT'])
def gpt3():

    data   = json.loads(request.get_data().decode('utf-8'))
    prompt = data["text"]

    if data["use_cached_prompt"]:
        prompt = _cached_prompt.format(prompt)

    try:  

        response = openai.Completion.create(engine="davinci", prompt=prompt, stop="Input:", temperature=0, max_tokens=300)
        return json.dumps( { 'result' : 'success', 'response' : response['choices'][0]['text'].strip() } )

    except Exception as e:
        return json.dumps( { 'result' : str(e) } )


''' main '''
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3456)))

