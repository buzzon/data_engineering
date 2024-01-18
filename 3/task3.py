from inspect import cleandoc
import re
from textwrap import dedent
import pandas as pd
from main import fixNumber, read_files_names, save_file, save_file_json
import xml.etree.ElementTree as ET

keys = {
    'name' : '(.*)',
    'constellation' : '(.*)',
    'spectral-class' : '(.*)',
    'radius' : '(.*)',
    'rotation' : '(.*) days',
    'age' : '(.*) billion years',
    'distance' : '(.*) million km',
    }

data = []

def clearText(text):
    return dedent(cleandoc(text)).replace('\n', '')

def execute(html):
    tree = ET.parse(html)
    root = tree.getroot() 
    result = {x: fixNumber(re.match(keys[x], clearText(root.find(x).text)).group(1)) for x in keys}
    data.append(result)

read_files_names(3, execute)

save_file_json(3, "task_1", data)
save_file_json(3, "task_2", sorted(data, key=lambda x: x['distance'], reverse=True))
save_file_json(3, "task_3", list(filter(lambda x: x['age'] < 5.2, data)))

df = pd.DataFrame(data)
save_file(3, "task_4", df['radius'].describe().to_json(force_ascii=True))
save_file(3, "task_5", df['constellation'].value_counts().to_json(force_ascii=False))
