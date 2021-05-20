import json

weight = 5

termDict = {}
for i in range(1,623):
    print(f'Processing Num: {i}')
    with open(f"output_data_{i}.json",'r') as loadFile:
        loadDict = json.load(loadFile)
        for key,value in loadDict.items():
            for sk,sv in value.items():

                if sk=='keywords':
                    for item in sv:
                        if (item in termDict) == False:
                            termDict[item] = {}

                        if key in termDict[item]:
                            termDict[item][key] = termDict[item][key] + 1
                        else:
                            termDict[item][key] = 1
                            
                if sk=='redirects':
                    for item in sv:
                        if (item in termDict) == False:
                            termDict[item] = {}

                        if key in termDict[item]:
                            termDict[item][key] = termDict[item][key] + weight
                        else:
                            termDict[item][key] = weight

with open("term.json","w") as f:
    json.dump(termDict,f)