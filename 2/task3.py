import json
import msgpack
import os
from os import path
from statistics import mean

parent_dir = path.dirname(path.abspath(__file__))

dataset = list()

with open(path.join(parent_dir, 'data', 'products_71.json'), 'r', encoding='utf-8') as inp:
    dataset = json.load(inp)

name_dictionary = dict()

for item in dataset:
    if item['name'] not in name_dictionary:
        name_dictionary[item['name']] = []

    name_dictionary.get(item['name']).append(item['price'])


def get_product_props(product_price_list: [int]):
    min_price = min(product_price_list)
    avg_price = mean(product_price_list)
    max_price = max(product_price_list)

    return min_price, avg_price, max_price


result_list = []

for product_name, values in name_dictionary.items():
    min_v, avg_v, max_v = get_product_props(values)
    result_list.append({
        'name': product_name,
        'min': min_v,
        'avg': avg_v,
        'max': max_v
    })

pjson = path.join(parent_dir, 'result', '3', 'products_71.json')
pmsgpack = path.join(parent_dir, 'result', '3', 'products_71.msgpack')

with open(pjson, 'w', encoding='utf-8') as out:
    out.write(json.dumps(result_list))

with open(pmsgpack, 'wb') as out:
    out.write(msgpack.packb(result_list))

sizejson = os.path.getsize(pjson)
smsgpack = os.path.getsize(pmsgpack)

print(f"json = {sizejson}")
print(f"msgpack = {smsgpack}")

print(sizejson / smsgpack)