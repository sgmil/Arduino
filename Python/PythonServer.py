# Test server
from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def home():
    nam = "Steve"
    print ("Requested")
    return "Hello,%s" %(nam)
    
@app.route('/json-post', methods = ['POST'])
def postjsonHandler():
    print (request.is_json)
    content = request.get_json()
    print (content)
    #print (content[1]["location"])
    return 'JSON posted'
    
if __name__ == "__main__":
    app.run(host='192.168.0.106',port=5050, debug=True)
