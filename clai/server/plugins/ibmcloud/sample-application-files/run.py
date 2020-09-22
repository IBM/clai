import json
import os

from flask import Flask, render_template, request
from flask_cors import CORS

""""""
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
CORS(app)


@app.route("/")
def hello():
    print("Application running!")
    return "Hello World!"


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8081)), debug=True
    )
