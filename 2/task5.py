import json
from os import path
import os
from statistics import mean
import msgpack
import pandas as pd

parent_dir = path.dirname(path.abspath(__file__))
output = path.join(parent_dir, 'result', '5', 'result')

with open(path.join(parent_dir, 'data', 'large-file.json'), 'r', encoding='utf-8') as inp:
    dataset = json.load(inp)

# type | str
# actor.id | int
# actor.login | str
# public | bool
# repo.name | str
# payload.description | str?
# payload.size | int?

def count(item, name, dict):
    if name in item:
        if item[name] not in dict:
            dict[item[name]] = 0
        dict[item[name]] += 1

def sort(dict):
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}

types = {}
ids = {}
logins = {}
publics = {}
names = {}
descriptions = {}
sizes = {}

for item in dataset:
    count(item, "type", types)
    count(item["actor"], "id", ids)     
    count(item["actor"], "login", logins)

    count(item, "public", publics)
    count(item["repo"], "name", names)
    # if ("description" in item["payload"]):
    #     descriptions.append(len(item["payload"]["description"]))
    count(item["payload"], "size", sizes) 

    if "description" in item["payload"]:
        l = len(str(item["payload"]["description"]))
        if l not in descriptions:
            descriptions[l] = 0
        descriptions[l] += 1


result = [{
    'types' : sort(types),
    'ids': {
        'cnt': sort(ids), 
        'avg': mean(ids.values()),
        'min': min(ids.values()),
        'max': max(ids.values()),
        'sum': sum(ids.values()),
    },
    'logins': sort(logins),
    'publics': sort(publics),
    'names': sort(names),
    'descriptions': {
        'cnt': sort(descriptions), 
        'avg': mean(descriptions.keys()),
        'min': min(descriptions.keys()),
        'max': max(descriptions.keys()),
        'sum': sum(descriptions.keys()),
    },
    'sizes': {
        'cnt': sort(sizes), 
        'avg': mean(sizes.values()),
        'min': min(sizes.values()),
        'max': max(sizes.values()),
        'sum': sum(sizes.values()),
    }
}]


df = pd.DataFrame([x for x in result])

with open(output + '.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result))

with open(output + '.msgpack', 'wb') as out:
    out.write(msgpack.packb(result))

with open(output + '.csv', 'w', encoding='utf-8') as out:
    out.write(df.to_csv(index=False))

df.to_pickle(output + '.pkl')

sjson = os.path.getsize(output + '.json')
smsgpack = os.path.getsize(output + '.msgpack')
scsv = os.path.getsize(output + '.csv')
spkl = os.path.getsize(output + '.pkl')

sizes = {
   "json" : sjson,
   "msgpack" : smsgpack,
   "csv" : scsv,
   "pkl" : spkl,
}

sizes['avg'] = mean(sizes.values())

for x in sorted(sizes.items(), key=lambda item: item[1], reverse=True):
    print(f"{x[0]}\tsize:{x[1]}\t{((x[1] / sizes['avg']) * 100) - 100}%")
