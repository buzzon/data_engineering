from os import path
import re

parent_dir = path.dirname(path.abspath(__file__))
quest = re.search(r'\d', path.basename(__file__)).group(0)

def job(lines):
    avg = []
    for line in lines:
        numbers = list(map(int, line.split('.')))
        count = len(numbers)
        avg.append(sum(numbers) / count)
    return avg

def result(data):
    with open(path.join(parent_dir, 'result', 'result_' + quest), "w") as file:
        for res in data:
            file.write(f"{res}\n")

def main():
    file = open(path.join(parent_dir, 'data', 'text_' + quest + '_var_71'), "r")
    lines = file.readlines()
    file.close()
    result(job(lines))

main()


