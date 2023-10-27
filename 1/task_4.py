from os import path
import re

parent_dir = path.dirname(path.abspath(__file__))
quest = re.search(r'\d', path.basename(__file__)).group(0)
var = 71

def job(lines):
    age_filter = var + (var % 10)
    summa = 0
    count = 0
    data = []
    for line in lines:
        row = line.split(',')
        summa += int(row[4][:-1])
        count += 1
        data.append((row[0], row[1], row[2], row[3], row[4]))
    avg_sum = summa / count
    data.sort(key=lambda x: x[0])
    data = filter(lambda row: int(row[4][:-1]) >= avg_sum and int(row[0]) > age_filter, data)
    return data

def result(data):
    with open(path.join(parent_dir, 'result', 'result_' + quest), "w") as file:
        for row in data:
            file.write( (', '.join(str(x) for x in row) + '\n'))

def main():
    file = open(path.join(parent_dir, 'data', 'text_' + quest + '_var_71'), "r")
    lines = file.readlines()
    file.close()
    result(job(lines))

main()


