import json
with open('log.json', 'r+') as f:
    data = json.load(f)
print(data)
for entry in data:
    print (type(data[entry]))