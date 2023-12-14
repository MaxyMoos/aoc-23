TEST = False

if TEST:
    fp = './test/input'
else:
    fp = './data/14/input'


def pretty(x):
    print('\n'.join(x))


def transpose(x):
    return [''.join([item[i] for item in x]) for i in range(len(x[0]))]


def move_Os(s):
    while '.O' in s:
        s = s.replace('.O', 'O.')
    return s


if __name__ == '__main__':
    with open(fp, 'r') as input_file:
        inp = [i.strip() for i in input_file.readlines() if len(i.strip())]
    t_input = transpose(inp)
    new_inp = []
    for line in t_input:
        new_inp.append(move_Os(line))
    new_inp = transpose(new_inp)

    score = 0
    for i, line in enumerate(new_inp):
        line_score = len(new_inp) - i
        score += sum([line_score for it in line if it == 'O'])

    print(score)
