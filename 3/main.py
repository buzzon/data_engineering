import json
from os import path, listdir, makedirs
import re
from inspect import cleandoc
from textwrap import dedent

from html.parser import HTMLParser

parent_dir = path.dirname(path.abspath(__file__))

def read_files(task, handle):
    for fname in listdir(path.join(parent_dir, 'data', str(task))):
        file = open(path.join(parent_dir, 'data', str(task), fname), "r")
        handle(file.read())
        file.close()
        # return

def read_files_names(task, handle):
    for fname in listdir(path.join(parent_dir, 'data', str(task))):
        handle(path.join(parent_dir, 'data', str(task), fname))
        # return

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

class MyHTMLParser(HTMLParser):
    data = dict()
    plenty = []
    current_attr = ""
    splitter = None

    def __init__(self, keys = {}, exclude = [], splitter = None, *args, **kwargs):
        self.keys = keys
        self.exclude = exclude
        self.splitter = splitter
        super(MyHTMLParser, self).__init__(*args, **kwargs)

    def handle_starttag(self, _, attrs):
        attr = next(filter(lambda x: x[0] == 'class' or x[0] == 'type', attrs), None)
        if (attr):
            self.current_attr = attr[1]

        if(self.splitter is not None and self.splitter == self.current_attr):
            if (len(self.data)): self.plenty.append(self.data)
            self.clear()
            
        
    def handle_data(self, data):
        data = dedent(cleandoc(data)).replace('\n', '')
        if (len(data) < 1): return
        if (self.current_attr not in self.exclude and self.current_attr):
            self.data[self.current_attr] = fixNumber(data)
            self.current_attr = None
        else:
            key = [x for x in self.keys if re.search(x, data)]
            if (len(key)):
                for k in key:
                    m = re.match(k, data)
                    self.data[self.keys.get(k)] = fixNumber(m.group(1))
            else:
                print("data with out class :", data, len(data))
    
    def close(self) -> None:
        self.clear()
        return super().close()
    
    def clear(self) -> None:
        self.data = dict()
        self.current_attr = ""

    def handle_endtag(self, tag: str) -> None:
        self.current_attr = ""
        return super().handle_endtag(tag)