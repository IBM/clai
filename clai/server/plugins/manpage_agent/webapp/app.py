#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
from flask import Flask, request, jsonify
from data import Datastore

app = Flask(__name__)
port = int(os.getenv("PORT", 5000))

_DATASTORE = Datastore()


@app.route("/", methods=["GET"])
def homepage():
    return "Agent up"


@app.route("/findManPage/", methods=["POST"])
def find_man_page():

    try:
        text = request.args.get("text", None)
        result_count = request.args.get("result_count", 1)
        result_count = int(result_count)

        if text is None:
            return

        result = _DATASTORE.search(text.strip(), result_count)

        commands = [x[0] for x in result]
        dists = [x[1] for x in result]
    except Exception as err:
        payload = {"result": "error", "message": str(err)}
    else:
        payload = {"status": "success", "commands": commands, "dists": dists}
    finally:
        return jsonify(payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(port))
