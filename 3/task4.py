from inspect import cleandoc
import re
from textwrap import dedent
import pandas as pd
from main import fixNumber, read_files_names, save_file, save_file_json
import xml.etree.ElementTree as ET

keys = {
    'id' : '(.*)',
    'name' : '(.*)',
    'category' : '(.*)',
    'size' : '(.*)',
    'color' : '(.*)',
    'material' : '(.*)',
    'price' : '(.*)',
    'rating' : '(.*)',
    'reviews' : '(.*)',
    'new' : '(.*)',
    'sporty' : '(.*)',
    }

data = []

def clearText(text):
    return dedent(cleandoc(text)).replace('\n', '')

def execute(html):
    tree = ET.parse(html)
    for cl in tree.getroot().findall("clothing"):
        result = {x: fixNumber(re.match(keys[x], clearText(cl.find(x).text)).group(1)) for x in keys if cl.find(x) is not None}
        data.append(result)

read_files_names(4, execute)

save_file_json(4, "task_1", data)
save_file_json(4, "task_2", sorted(data, key=lambda x: x['price'], reverse=True))
save_file_json(4, "task_3", list(filter(lambda x: x['rating'] > 4.9, data)))

df = pd.DataFrame(data)
save_file(4, "task_4", df['reviews'].describe().to_json(force_ascii=True))
save_file(4, "task_5", df['material'].value_counts().to_json(force_ascii=False))
