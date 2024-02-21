from flask import Flask, jsonify
import time
from llm_loader import load_module
app = Flask(__name__)


llm = load_module()
@app.route('/chat',methods=['GET'])
def respond_with_llm():
    print("handling requests")
    response = llm({'query':'what is malware analysis?'})
    return response['result']

def run_server():
    app.run(debug=True)

run_server()