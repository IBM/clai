#!/usr/bin/env python3

"""
imports
"""
from flask import Flask, request, render_template
from typing import Dict

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import json
import os
import inspect

"""
globals
"""

config = json.loads(open("config.json").read())

authenticator = IAMAuthenticator(config["i_am_id"])
assistant = AssistantV2(version="2020-13-05", authenticator=authenticator)

assistant.set_service_url("https://gateway.watsonplatform.net/assistant/api")

""""""
app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to the router for the WA instances for the nlc2cmd skill in CLAI."


"""
endpoint for tarbot
"""


@app.route("/tarbot", methods=["GET", "POST", "PUT"])
def tarbot():
    return get_response(
        assistant_id=config["skills"][inspect.stack()[0][3]],
        data=json.loads(request.get_data().decode("utf-8")),
    )


"""
endpoint for grepbot
"""


@app.route("/grepbot", methods=["GET", "POST", "PUT"])
def grepbot():
    return get_response(
        assistant_id=config["skills"][inspect.stack()[0][3]],
        data=json.loads(request.get_data().decode("utf-8")),
    )


"""
endpoint for zosbot
"""


@app.route("/zosbot", methods=["GET", "POST", "PUT"])
def zosbot():
    return get_response(
        assistant_id=config["skills"][inspect.stack()[0][3]],
        data=json.loads(request.get_data().decode("utf-8")),
    )


""" get response from WA workspace """


def get_response(assistant_id: str, data: Dict) -> Dict:

    try:

        session_info = assistant.create_session(assistant_id=assistant_id).get_result()
        response = assistant.message(
            assistant_id=assistant_id,
            session_id=session_info["session_id"],
            input={
                "message_type": "text",
                "text": data["text"],
                "options": {"alternate_intents": True},
            },
        ).get_result()

        return json.dumps({"result": "success", "response": response})

    except Exception as e:
        return json.dumps({"result": str(e)})


""" main """
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3456)))
