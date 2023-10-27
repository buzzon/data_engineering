import pandas
from os import path
import re

parent_dir = path.dirname(path.abspath(__file__))
quest = re.search(r'\d', path.basename(__file__)).group(0)

input = path.join(parent_dir, 'data', 'text_' + quest + '_var_71')
output = path.join(parent_dir, 'result', 'result_' + quest)

pandas.read_html(open(input, 'r').read())[0].to_csv(output)