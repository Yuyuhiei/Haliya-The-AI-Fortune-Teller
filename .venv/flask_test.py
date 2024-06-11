from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def test():
    return jsonify({'flask status': 'running'})

app.run()