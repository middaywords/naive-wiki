import json

permutermIndex = {}
with open(f"term-doc3.json",'r') as loadFile:
    loadDict = json.load(loadFile)
    for key in loadDict.keys():
        newKey = key+'$'
        for i in range(len(newKey)):
            if (newKey[0] in permutermIndex) == False:
                permutermIndex[newKey[0]] = {}

            permutermIndex[newKey[0]][newKey] = key
            newKey = newKey[len(newKey)-1] + newKey[0:len(newKey)-1]

with open("permutermIndex.json","w") as f:
    json.dump(permutermIndex,f)
