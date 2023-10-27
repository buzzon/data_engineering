from os import path
import re

parent_dir = path.dirname(path.abspath(__file__))
quest = re.search(r'\d', path.basename(__file__)).group(0)

def job(lines):
    result = []
    for line in lines:
        numbers = line.split(',')
        for i in range(len(numbers) - 1):
            if numbers[i].isdigit():
                number = int(numbers[i])
            else:
                number = (int(numbers[i - 1]) + int(numbers[i + 1])) / 2
            if number ** 0.5 >= 50 + int(quest):
                result.append(number)
    return result

def result(data):
    with open(path.join(parent_dir, 'result', 'result_' + quest), "w") as file:
        for number in data:
            file.write(f"{int(number)}\n")

def main():
    file = open(path.join(parent_dir, 'data', 'text_' + quest + '_var_71'), "r")
    lines = file.readlines()
    file.close()
    result(job(lines))

main()


