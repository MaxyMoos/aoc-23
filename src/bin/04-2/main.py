with open('./data/04-1/input', 'r') as input_file:
    input = input_file.readlines()


input = [item for item in input if len(item)]
waiting_list = {i: 0 for i in range(len(input))}


def process_line(line_idx, line):
    _, numbers = line.split(':')

    winning, own = numbers.split('|')
    winning = winning.strip().split(' ')
    winning = [i for i in winning if len(i)]
    own = own.strip().split(' ')
    own = [i for i in own if len(i)]

    n = 0
    for cur in own:
        if cur in winning:
            n += 1
    if n > 0:
        for i in range(1, n+1):
            waiting_list[line_idx + i] += 1

    for i in range(1, n+1):
        waiting_list[line_idx + i] += waiting_list[line_idx]


for line_idx, line in enumerate(input):
    process_line(line_idx, line)
print(len(input) + sum(waiting_list.values()))
