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

@functools.cache
def is_crossing(node):
    s = nodes.index(node)
    i = 1
    prev_node, next_node = node, node
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

def is_inside_loop(x, y):
    intersections = 0
    row_length = bottom - top

    left = [i for i in nodes if i[0] == x and i[1] < y and is_crossing(i)[0]]
    left_nodes = []
    for item in left:
        if is_crossing(item)[1] not in map(lambda a: is_crossing(a)[1], left_nodes):
            left_nodes.append(item)
    return len(left_nodes) % 2 != 0

def find_points_inside_loop():
    inside_points = []
    for x in range(top, bottom + 1):
        for y in range(left, right + 1):
            if is_inside_loop(x, y):
                inside_points.append((x, y))
    return inside_points

print(len(set(find_points_inside_loop() + nodes)))
