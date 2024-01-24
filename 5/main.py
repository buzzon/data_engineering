from bson import json_util
from os import path, makedirs
import pickle
import re
import sqlite3
import csv

parent_dir = path.dirname(path.abspath(__file__))

def load_pickle(file_name:str):
    with open(path.join(parent_dir, 'data', file_name), "rb") as file:
        data_file = pickle.load(file)
    return data_file

def save_file(task, name, data):
    makedirs(path.join(parent_dir, 'result', str(task)), exist_ok=True)
    with open(path.join(parent_dir, 'result', str(task), str(name) + '.json'), 'w', encoding='utf-8') as result:
        result.write(data)

def save_file_json(task, name, data):
    save_file(task, name, json_util.dumps(data, ensure_ascii=False))

def fixNumber(data):
    if (re.search('^-?\d+(?:\.\d+)$', str(data)) is not None): data = float(data)
    elif (re.search('^[\ \d]+$', str(data)) is not None): data = int(str(data).replace(" ", ""))
    return data

def read_file(fname, handle):
    file = open(path.join(parent_dir, 'data', fname), "r")
    data = handle(file.readlines())
    file.close()
    return data


def read_csv(fname, delimiter):
    file = open(path.join(parent_dir, 'data', fname), "r")
    data = csv.DictReader(file, delimiter=delimiter)
    data = [{x: fixNumber(d[x]) for x in d} for d in data]
    file.close()
    return data