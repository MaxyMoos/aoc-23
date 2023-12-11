import re
import sys


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
cur = (starting_point[0], starting_point[1]+1)  # hardcoded
loop = [starting_point, cur]
next_dirs = DIRMAP.get(inputmap.get(*cur))  # allowed directions given the current node character
next_nodes = get_neighbors(cur)  # all neighbors
next_nodes = [item for i, item in enumerate(next_nodes) if next_dirs[i] and not item == prev]  # filter with allowed directions
nb_ok = valid_neighbors(next_nodes)


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
    loop.append(cur)
loop = loop[:-1]


total = 0
top_limit = min(item[0] for item in loop)
bottom_limit = max(item[0] for item in loop)
left_limit = min(item[1] for item in loop)
right_limit = max(item[1] for item in loop)


def check_hcrossings(loop_nodes_text):
    nodes = loop_nodes_text.replace('S', '-')  # hardcoded
    nodes = re.sub(r"F(-+)?7", '', nodes)
    nodes = re.sub(r"L(-+)?J", '', nodes)
    nodes = re.sub(r"L(-+)?7", '|', nodes)
    nodes = re.sub(r"F(-+)?J", '|', nodes)
    return len(nodes)


def check_vcrossings(loop_nodes_text):
    nodes = loop_nodes_text.replace('S', '-')  # hardcoded
    nodes = re.sub(r"7(\|+)?L", '-', nodes)
    nodes = re.sub(r"F(\|+)?L", '', nodes)
    nodes = re.sub(r"F(\|+)?J", '-', nodes)
    nodes = re.sub(r"7(\|+)?J", '', nodes)
    return len(nodes)


for i in range(top_limit, bottom_limit + 1):
    for j in range(left_limit, right_limit + 1):
        node = (i, j)

        if node in loop:
            continue

        if i in (0, len(inp) - 1) or j in (0, len(inp[0]) - 1):
            continue

        left_loop_nodes = ''.join([inputmap.get(*item) for item in sorted(filter(lambda l: l[0] == i and l[1] < j, loop))]) # loop nodes on the left, same line as current node
        right_loop_nodes = ''.join([inputmap.get(*item) for item in sorted(filter(lambda l: l[0] == i and l[1] > j, loop))])
        top_loop_nodes = ''.join([inputmap.get(*item) for item in sorted(filter(lambda l: l[1] == j and l[0] < i, loop))])
        bottom_loop_nodes = ''.join([inputmap.get(*item) for item in sorted(filter(lambda l: l[1] == j and l[0] > i, loop))])

        lh = check_hcrossings(left_loop_nodes)
        if lh == 0:
            continue
        elif lh % 2 == 1:
            total += 1
            continue
        rh = check_hcrossings(right_loop_nodes)
        if rh == 0:
            continue
        elif rh % 2 == 1:
            total += 1
            continue
        tv = check_vcrossings(top_loop_nodes)
        if tv == 0:
            continue
        elif tv % 2 == 1:
            total += 1
            continue
        bv = check_vcrossings(bottom_loop_nodes)
        if bv == 0:
            continue
        elif bv % 2 == 1:
            total += 1
            continue

print(total)
