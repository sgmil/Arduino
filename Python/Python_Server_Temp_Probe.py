# Python Server for Temp Probes #


class Probe():
    def __init__(self, place, name, tmax, tmin):
        self.place=place
        self.name=name
        self.tmax=tmax
        self.tmin=tmin
    
    def tooHot(self):
        if (self.current>self.tmax):
            print("Too Hot")

    def tooCold(self):
        if (self.current<self.tmin):
            print("Too Cold")

def updateTemp(pl):
    for i in pl.keys():
        pl[i].current=e[(pl[i].place)][i]
        pl[i].tooHot()
        pl[i].tooCold()
        
Garage={"fridge":Probe("Garage", "fridge", 39,33),\
        'freezer':Probe("Garage","freezer",24,0),\
        'ambient':Probe("Garage","ambient",100,0)}

e={"Garage":{"freezer":-2,"fridge":42,"ambient":67}}

if ([*e.keys()][0]=="Garage"):
    updateTemp(Garage)


    #Garage["fridge"].current=e["Garage"]["fridge"]
    #Garage["fridge"].tooHot()
