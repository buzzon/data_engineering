import requests
import json
from os import path

parent_dir = path.dirname(path.abspath(__file__))
output = path.join(parent_dir, 'result', '5', 'result')

API_URL="https://raw.githubusercontent.com/json-iterator/test-data/master/large-file.json"

res = requests.get(API_URL)
jsonData = json.loads(res.text)

# print(jsonData)

# with open(output, "w") as res:
#     # res.write(jsonData)
#     res.writelines(res)