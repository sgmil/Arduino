# Python Server for Temp Probes #
from flask import Flask, request
import json
app = Flask(__name__)

class Probe():
    def __init__(self, place, name, tmax, tmin):
        self.place=place
        self.name=name
        self.tmax=tmax
        self.tmin=tmin
    
    def tooHot(self):
        print("%s %s is:" %(self.place,self.name))
        if (self.current>self.tmax):
            print("Too Hot.")
        else:
            print("Not too hot")
            

    def tooCold(self):
        print("%s %s is:" %(self.place,self.name))
        if (self.current<self.tmin):
            print("Too Cold")
        else:
            print("Not too cold.")

def updateTemp(pldict, pljson):
    print("updating...")
    for i in pldict.keys():
        print(i)
        print(pljson[[*pljson.keys()][0]][i])
        
        pldict[i].current=pljson[[*pljson.keys()][0]][i]
        pldict[i].tooHot()
        pldict[i].tooCold()
        print("Temp checked")
        
Garage={"fridge":Probe("Garage", "fridge", 39,33),\
        'freezer':Probe("Garage","freezer",24,0),\
        'ambient':Probe("Garage","ambient",100,0)}

e={"Garage":{"freezer":-2,"fridge":42,"ambient":67}}



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
    print(type(content))
    #json_content=json.loads(content)
    #print (content[1]["location"])
    print([*content.keys()][0])
    print(type([*content.keys()][0]))
    if (([*content.keys()][0])=="Garage"):
        updateTemp(Garage,content)
    return 'JSON posted'
    
if __name__ == "__main__":
    app.run(host='192.168.0.106',port=5050, debug=True)
