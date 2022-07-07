import maya.cmds as mc
import os
import json

optionsPath = 'Plugin/scripts/options.json'
optionsAbsolutePath = os.path.join(os.path.split(mc.file(q=True, loc=True))[0], optionsPath)

def getOptions():
    return json.load(open(optionsAbsolutePath))

def updateOptions(type,option,value):
    options = getOptions()
    options[type][option] = value
    with open(optionsAbsolutePath, 'w') as file:
        json.dump(options, file)  

if __name__ == "__main__":
    updateOptions("style_transfer","itterations","200") 
    updateOptions("style_transfer","itterations","400") 