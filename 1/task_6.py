import requests
import json
from json2html import *
from os import path
import re

parent_dir = path.dirname(path.abspath(__file__))
quest = re.search(r'\d', path.basename(__file__)).group(0)
output = path.join(parent_dir, 'result', 'result_' + quest)

API_URL="https://jsonapi.org/alt-favicons/manifest.json"

res = requests.get(API_URL)
jsonData = json.loads(res.text)
# print(json2html.convert(json = jsonData))

with open(output, "w") as res:
    res.write(json2html.convert(json = jsonData))