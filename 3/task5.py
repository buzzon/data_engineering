from inspect import cleandoc
import re
from textwrap import dedent
import pandas as pd
from main import fixNumber, read_files_names, save_file, save_file_json
import xml.etree.ElementTree as ET
import requests 
from bs4 import BeautifulSoup 
from task3 import clearText

paths = [
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/kaplya/16654/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/kaplya/16655/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/kaplya/19989/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/tsilindr/7267/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/kaplya/19988/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/kaplya/71602/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/kaplya/19988/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/kaplya/71602/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/plamya/30107/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/plamya/22248/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/tsilindr/73088/",
    "https://kmiz-online.ru/catalog/nogtevoy_servis/almaznye_nasadki/konus/71607/",
]


result = []

for p in paths:
    data = dict()
    r = requests.get(p) 
    parsed_html = BeautifulSoup(r.content, 'html5lib')
    data['preview_text'] = parsed_html.body.find('div', attrs={'class':'preview_text'}).text
    data['price_value'] = fixNumber(parsed_html.body.find('span', attrs={'class':'price_value'}).text)
    result.append(data)


save_file_json(5, "task_1_1", result)
save_file_json(5, "task_1_2", sorted(result, key=lambda x: x['price_value'], reverse=True))



result2 = []

p = "https://kmiz-online.ru/catalog/podologiya_/almaznye_golovki/?PAGEN_1=2"
r = requests.get(p) 
parsed_html = BeautifulSoup(r.content, 'html5lib')
pos = parsed_html.body.find_all('div', attrs={'class':'item_block js-notice-block grid-list__item grid-list-border-outer'})
for p in pos:
    data = dict()
    data['item-title'] = clearText(p.find('div', attrs={'class':'item-title'}).text)
    data['price_value'] = fixNumber(clearText(p.find('span', attrs={'class':'price_value'}).text))
    result2.append(data)

save_file_json(5, "task_2_1", result2)
save_file_json(5, "task_2_2", sorted(result2, key=lambda x: x['price_value'], reverse=True))