import json
from os import path, makedirs
import pickle
import re
import sqlite3
import csv

parent_dir = path.dirname(path.abspath(__file__))


def read_file(fname, handle):
    file = open(path.join(parent_dir, 'data', fname), "r")
    data = handle(file.readlines())
    file.close()
    return data


def read_json(fname):
    file = open(path.join(parent_dir, 'data', fname), "r")
    data = json.load(file)
    file.close()
    return data

def read_csv(fname, delimiter):
    def fix_row(row):
        if len(row) == 6:
            row.insert(3,'none')
        return row

    file = open(path.join(parent_dir, 'data', fname), "r")
    data = csv.reader(file, delimiter=delimiter)
    data = [fix_row(x) for x in data if len(x)]
    title = data.pop(0)
    title[3] = 'type'
    file.close()
    return [title, data]

def load_pickle(file_name:str):
    with open(path.join(parent_dir, 'data', file_name), "rb") as file:
        data_file = pickle.load(file)
    return data_file

def connect_to_database(task:int):
    connection = sqlite3.connect(path.join(parent_dir, 'result', str(task) + ".sqlite",))
    connection.row_factory = sqlite3.Row
    return connection

def save_file(task, name, data):
    makedirs(path.join(parent_dir, 'result', str(task)), exist_ok=True)
    with open(path.join(parent_dir, 'result', str(task), str(name) + '.json'), 'w', encoding='utf-8') as result:
        result.write(data)

def save_file_json(task, name, data):
    save_file(task, name, json.dumps(data, ensure_ascii=False))

def fixNumber(data):
    if (re.search('^-?\d+(?:\.\d+)$', str(data)) is not None): data = float(data)
    elif (re.search('^[\ \d]+$', str(data)) is not None): data = int(str(data).replace(" ", ""))
    return data


def query(db, operation, params=None):
    cursor = db.cursor()

    res = cursor.execute(operation, params)
    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(dict(row))
    cursor.close()

    return items_list