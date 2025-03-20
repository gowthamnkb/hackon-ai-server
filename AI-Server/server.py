import json

from flask import Flask, request, jsonify
from core import ProcessModel
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/action", methods=["POST"])
def health_check():
    data = request.json
    return jsonify({"response": ProcessModel().process(data)}), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
