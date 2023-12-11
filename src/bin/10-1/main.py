#with open('./test/input', 'r') as input_file:
with open('./data/10-1/input', 'r') as input_file:
    inp = input_file.readlines()
    inp = [line.strip() for line in inp if len(line.strip())]


class Map():
    def __init__(self, inp):
        self._input = inp

    def get(self, x, y):
        return self._input[x][y]


inputmap = Map(inp)
for i, line in enumerate(inp):
    if 'S' in line:
        starting_point = i, line.index('S')


def get_neighbors(point):
    """ Returns neighbors of a point (x, y) under the form of a UP, DOWN, LEFT, RIGHT coords list """
    x, y = point[0], point[1]
    nb = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1)
    ]
    for i, item in enumerate(nb):
        if 0 <= item[0] <= len(inp) and 0 <= item[1] <= len(inp[0]):
            continue
        else:
            nb[i] = False
    return nb


def valid_neighbors(neighbors):
    OK_UP = ['|', '7', 'F', 'S']
    OK_DOWN = ['|', 'L', 'J', 'S']
    OK_LEFT = ['-', 'L', 'F', 'S']
    OK_RIGHT = ['-', 'J', '7', 'S']
    OK_ALL = [OK_UP, OK_DOWN, OK_LEFT, OK_RIGHT]

    ret = [item for i, item in enumerate(neighbors) if inputmap.get(*item) in OK_ALL[i]]
    return ret


DIRMAP = { # UP, DOWN, LEFT, RIGHT
    'S': [True, True, True, True],
    '-': [False, False, True, True],
    '|': [True, True, False, False],
    'L': [True, False, False, True],
    'J': [True, False, True, False],
    '7': [False, True, True, False],
    'F': [False, True, False, True],
}

prev = starting_point
cur = (starting_point[0], starting_point[1]+1)
next_dirs = DIRMAP.get(inputmap.get(*cur))  # allowed directions given the current node character
next_nodes = get_neighbors(cur)  # all neighbors
next_nodes = [item for i, item in enumerate(next_nodes) if next_dirs[i] and not item == prev]  # filter with allowed directions
nb_ok = valid_neighbors(next_nodes)

count = 1
while cur != starting_point:
    next_dirs = DIRMAP.get(inputmap.get(*cur))  # allowed directions given the current node character
    next_nodes = get_neighbors(cur)  # all neighbors
    next_nodes = [item for i, item in enumerate(next_nodes) if next_dirs[i] and not item == prev]  # filter with allowed directions
    nb_ok = valid_neighbors(next_nodes)
    if len(next_nodes) == 1:
        prev = cur
        cur = next_nodes[0]
    else:
        print(f"Issue: cur = {cur}, next_nodes = {next_nodes}")
        break
    count += 1

print(count // 2)
