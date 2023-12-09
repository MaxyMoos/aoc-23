with open('./data/09-1/input', 'r') as input_file:
    inp = input_file.readlines()
    inp = [line.strip() for line in inp if len(line.strip())]


inp = [[int(i) for i in x.split()] for x in inp]

total = 0
for line in inp:
    diffs = [line]
    new_diff = [line[i+1] - line[i] for i in range(len(line) - 1)]
    while list(set(new_diff)) != [0]:
        diffs.append(new_diff)
        new_diff = [diffs[-1][i+1] - diffs[-1][i] for i in range(len(diffs[-1])-1)]
    diffs.append(new_diff)

    diffs[-1].insert(0, 0)
    for i in range(1, len(diffs)):
        diffs[-1-i].insert(0, diffs[-i-1][0] - diffs[-i][0])

    total += diffs[0][0]

print(total)
