import json

from flask import Flask, request
from core import ProcessModel


app = Flask(__name__)


@app.route("/action", methods=["GET"])
def health_check():
    data = request.json
    return {"response":json.dumps(ProcessModel().process(data))}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
