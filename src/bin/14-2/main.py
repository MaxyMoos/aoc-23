TEST = False


if TEST:
    fp = './test/input'
else:
    fp = './data/14/input'


with open(fp, 'r') as input_file:
    inp = [i.strip() for i in input_file.readlines() if len(i.strip())]


def pretty(x):
    print('\n'.join(x))


def transpose(x):
    return [''.join([item[i] for item in x]) for i in range(len(x[0]))]


def O_move_left(s):
    while '.O' in s:
        s = s.replace('.O', 'O.')
    return s


def O_move_right(s):
    while 'O.' in s:
        s = s.replace('O.', '.O')
    return s


def move_top(m):
    ret = []
    t_m = transpose(m)
    for line in t_m:
        ret.append(O_move_left(line))
    return transpose(ret)


def move_right(m):
    ret = []
    for line in m:
        ret.append(O_move_right(line))
    return ret


def move_left(m):
    ret = []
    for line in m:
        ret.append(O_move_left(line))
    return ret


def move_bottom(m):
    t_m = transpose(m)
    ret = []
    for line in t_m:
        ret.append(O_move_right(line))
    return transpose(ret)


def get_score(m):
    score = 0
    for i, line in enumerate(m):
        line_score = len(m) - i
        score += sum([line_score for i in line if i == 'O'])
    return score


if __name__ == '__main__':
    # move north = transpose + move left
    # move west = just move left
    # move east = just move right
    # move south = transpose + move right
    c_count = 0
    c_limit = 1000000000
    cycle_size = None
    previous_iters = [inp]
    while c_count != c_limit:
        inp = move_right(move_bottom(move_left(move_top(inp))))
        for i, item in enumerate(previous_iters):
            if inp == item:
                cycle_size = i+1
                break
        c_count += 1
        if cycle_size is not None:
            break
        else:
            previous_iters.insert(0, inp)

    idx = (c_limit - c_count) % cycle_size + c_count
    print(get_score(previous_iters[cycle_size-idx-1]))
