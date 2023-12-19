import functools
import sys

TEST = False
if TEST:
    fp = './test/input_18'
else:
    fp = './data/18/input'


with open(fp, 'r') as inputfile:
    inp = [i.strip() for i in inputfile.readlines() if len(i.strip())]

start = (0, 0)
m = []

nodes = [start]
DIRECTIONS = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
for line in inp:
    direction, length, color = line.split(' ')
    length = int(length)
    m.append((direction, length, color))
    for _ in range(length):
        nodes.append((nodes[-1][0] + DIRECTIONS[direction][0], nodes[-1][1] + DIRECTIONS[direction][1]))

# shift all nodes so we don't handle negative coords
if any([n[0] < 0 or n[1] < 0 for n in nodes]):
    top = min(n[0] for n in nodes)
    left = min(n[1] for n in nodes)
    nodes = [(n[0] - top, n[1] - left) for n in nodes]

def pretty(nodes):
    top = min(n[0] for n in nodes)
    left = min(n[1] for n in nodes)
    bottom = max(n[0] for n in nodes)
    right = max(n[1] for n in nodes)
    with open('./output', 'w') as output:
        for i in range(top, bottom + 1):
            cur_line = []
            for j in range(left, right + 1):
                node = (i,j)
                if node in nodes:
                    cur_line.append('#')
                else:
                    cur_line.append('.')
            output.write(''.join(cur_line))
            output.write('\n')

top = min(n[0] for n in nodes)
left = min(n[1] for n in nodes)
bottom = max(n[0] for n in nodes)
right = max(n[1] for n in nodes)
dug_nodes = []

#nodes = set(nodes)

@functools.cache
def is_crossing(node, direction):
    s = nodes.index(node)
    i = 1
    prev_node, next_node = node, node
    if direction == 'h':
        prev_node = nodes[(s-1)%len(nodes)]
        while prev_node[0] == node[0]:  # we're on the same line
            i += 1
            prev_node = nodes[(s-i)%len(nodes)]
        i = 1
        next_node = nodes[(s+1)%len(nodes)]
        while next_node[0] == node[0]:
            i += 1
            next_node = nodes[(s+i)%len(nodes)]
        return (prev_node[0] != next_node[0], (prev_node, next_node))
    else:
        prev_node = nodes[(s-1)%len(nodes)]
        while prev_node[1] == node[1]:  # same column
            i += 1
            prev_node = nodes[(s-i)%len(nodes)]
        i = 1
        next_node = nodes[(s+1)%len(nodes)]
        while next_node[1] == node[1]:
            i += 1
            next_node = nodes[(s+i)%len(nodes)]
        return (prev_node[1] != next_node[1], (prev_node, next_node))

expected = [
    0, 8, 8, 8, 14, 14, 18, 18, 31,
    31, 31, 31, 31, 49, 56, 56, 46, 49, 49,
    49, 49, 35, 41, 41, 47, 47, 47, 47, 49
]
expected = {k:v for k, v in enumerate(expected)}


LIMIT = 2
for i in range(top, bottom + 1):
    start_len_dug = len(dug_nodes)
    for j in range(left, right + 1):
        node = (i, j)

        if node in dug_nodes or node in nodes:
            continue

        if i in (0, bottom) or j in (0, right):
            continue

        left_loop_nodes = sorted([item for item in nodes if item[0] == i and item[1] < j and is_crossing(item, 'h')[0]])
        left_nodes = []
        for item in left_loop_nodes:
            if is_crossing(item, 'h')[1] not in map(lambda a: is_crossing(a, 'h')[1], left_nodes):
                left_nodes.append(item)

        right_loop_nodes = sorted([item for item in nodes if item[0] == i and item[1] > j and is_crossing(item, 'h')[0]])
        right_nodes = []
        for item in right_loop_nodes:
            if is_crossing(item, 'h')[1] not in map(lambda a: is_crossing(a, 'h')[1], right_nodes):
                right_nodes.append(item)

        top_loop_nodes = sorted([item for item in nodes if item[1] == j and item[0] < i and is_crossing(item, 'v')[0]])
        top_nodes = []
        for item in top_loop_nodes:
            if is_crossing(item, 'v')[1] not in map(lambda a: is_crossing(a, 'v')[1], top_nodes):
                top_nodes.append(item)

        bottom_loop_nodes = sorted([item for item in nodes if item[1] == j and item[0] > i and is_crossing(item, 'v')[0]])
        bottom_nodes = []
        for item in bottom_loop_nodes:
            if is_crossing(item, 'v')[1] not in map(lambda a: is_crossing(a, 'v')[1], bottom_nodes):
                bottom_nodes.append(item)

        if len(left_nodes) == 0 or len(right_nodes) == 0 or len(top_nodes) == 0 or len(bottom_nodes) == 0:
            continue

        if len(left_nodes) % 2 == 1 or len(right_nodes) % 2 == 1 or len(top_nodes) % 2 == 1 or len(bottom_nodes) % 2 == 1:
            dug_nodes.append(node)
    end_len_dug = len(dug_nodes)
    line_count = end_len_dug - start_len_dug
"""    if expected.get(i, 0) != line_count:
        print(f"Line {i+1}: {end_len_dug-start_len_dug} nodes detected in the loop vs {expected.get(i)} expected")
    else:
        print(f"Line {i+1}: OK")"""

print(len(set(dug_nodes)) + len(set(nodes)))
