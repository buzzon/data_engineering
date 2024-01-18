from main import read_files, MyHTMLParser, save_file, save_file_json
import pandas as pd

keys = {
    'Описание(.*)':'description', 
    'ISBN:(.*)': 'isbn', 
    'Рейтинг: (.*)': 'rate', 
    'Просмотры: (.*)': 'views',
    'Категория: (.*)': 'book-wrapper',
    'Объем: (.*) страниц': 'pages',
    'Издано в (.*)':'year',
    }

exclude = ['book-wrapper', 'pages', 'year']
parser = MyHTMLParser(keys, exclude)

data = []
def execute(html):
    parser.feed(html)
    data.append(parser.data)
    parser.close()

read_files(1, execute)

save_file_json(1, "task_1", data)
save_file_json(1, "task_2", sorted(data, key=lambda x: x['rate'], reverse=True))
save_file_json(1, "task_3", list(filter(lambda x: x['year'] > 2020, data)))

df = pd.DataFrame(data)
save_file(1, "task_4", df['views'].describe().to_json(force_ascii=True))
save_file(1, "task_5", df['author-p'].value_counts().to_json(force_ascii=False))
