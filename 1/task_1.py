from os import path
import re

parent_dir = path.dirname(path.abspath(__file__))
quest = re.search(r'\d', path.basename(__file__)).group(0)

def job(lines):
    frequency = dict()
    chars = '!?.,'
    for line in lines:
        for c in chars:
            line = line.replace(c, ' ')
        words = line.split()
        for word in words:
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1
    
    return dict(sorted(frequency.items(), reverse=True, key=lambda item: item[1]))

def result(data):
    with open(path.join(parent_dir, 'result', 'result_' + quest), "w") as file:
        for item in data.items():
             file.write(f"{item[0]}:{item[1]}\n")

def main():
    file = open(path.join(parent_dir, 'data', 'text_' + quest + '_var_71'), "r")
    lines = file.readlines()
    file.close()
    result(job(lines))

main()


