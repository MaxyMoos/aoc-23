import math

with open('./data/04-1/input', 'r') as input_file:
    input = input_file.readlines()

sum = 0
for line_idx, line in enumerate(input):
    tmp, numbers = line.split(':')
    card_id = tmp.split(' ')[1]

    winning, own = numbers.split('|')
    winning = winning.strip().split(' ')
    winning = [i for i in winning if len(i)]
    own = own.strip().split(' ')
    own = [i for i in own if len(i)]

    score = 0
    n = 0
    for cur in own:
        if cur in winning:
            n += 1
    sum += int(math.pow(2, n-1))
print(sum)
