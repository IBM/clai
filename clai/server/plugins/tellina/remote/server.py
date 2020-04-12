from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from translate_cmd import translate_clai
import os
import json

app = Flask(__name__)
CORS(app)

port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/api/translate', methods=['POST'])
def translateTest():
    cmd = request.json['command']
    jsonResp = translate_clai(cmd)
    return jsonify(jsonResp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
