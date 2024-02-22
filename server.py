from flask import Flask, jsonify,request
import time
from llm_loader import load_module
app = Flask(__name__)


llm = load_module()
@app.route('/query',methods=['POST'])
def respond_with_llm():
    print("handling requests")
    query = ""
    try:
        response = request.get_json()
        print("response",response)
        query = response["query"]
    except Exception as e:
        print("failed to obtain query from body",e)
        return "failed to obtain query from body"
    
    response = llm({'query':query})
    print(response)
    #return query
    llm_response={
        "query":query,
        "response":response["result"]
    }
    return jsonify(llm_response)

def run_server():
    app.run(debug=True)

run_server()