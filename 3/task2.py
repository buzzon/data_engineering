import pandas as pd
from main import read_files, MyHTMLParser, save_file, save_file_json
# from task1 import save_data

keys = {
    '(.*)" .*GB': 'diagonal',
    '.*" (.*) .*GB': 'model',
    '.*" .* (\d*)GB': 'memory',

    '(.*) ₽':'price', 
    '\+ начислим (.*) бонусов':'bonus',
    '(.*) ГГц': 'hHz',
    '(.*) GB': 'ram',
    '(.*) SIM': 'sim',
    '(.*) MP': 'camera',
    '(.*) мА \* ч': 'acc',
    }

exclude = [
    'ram',
    'sim',
    'camera',
    'acc'
    ]
parser = MyHTMLParser(keys, exclude, splitter="product-item")

data = []
def execute(html):
    parser.feed(html)
    data.extend(parser.plenty)
    parser.close()

read_files(2, execute)

save_file_json(2, "task_1", data)
save_file_json(2, "task_2", sorted(data, key=lambda x: x['price'], reverse=True))
save_file_json(2, "task_3", list(filter(lambda x: x['diagonal'] < 5.2, data)))

df = pd.DataFrame(data)
save_file(2, "task_4", df['bonus'].describe().to_json(force_ascii=True))
save_file(2, "task_5", df['matrix'].value_counts().to_json(force_ascii=False))
