
e={"Garage":{"freezer":12,"fridge":36}}
print([*e.keys()][0])
print(list(e)[0])
print(e["Garage"]["freezer"])
print(e[list(e)[0]]["freezer"])
print("Fridge is: "+ str(e[list(e)[0]]["fridge"]))
s="fridge"
print("{} {} is: {}".format(list(e)[0],s,e[list(e)[0]][s]))
