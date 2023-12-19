import math

TEST = False
if TEST:
    fp = './test/input_18'
else:
    fp = './data/18/input'


with open(fp, 'r') as inputfile:
    inp = [i.strip() for i in inputfile.readlines() if len(i.strip())]

start = (0, 0)
nodes = [start]
perimeter = 0

for line in inp:
    _direction, _length, color = line.split(' ')
    color = color[2:-1]
    length = int(color[:-1], 16)
    direction = {'0': (0, 1), '1': (1, 0), '2': (0, -1), '3': (-1, 0)}.get(color[-1])
    nodes.append((nodes[-1][0] + length * direction[0], nodes[-1][1] + length * direction[1]))
    perimeter += length

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

def surface(polygon):
    """ computed using the shoelace formula """
    A = 0
    for i in range(1, len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i-1]
        A += x1 * y2 - x2 * y1
    return int(abs(A/2))

def count_perimeter_length(polygon):
    cnt = 0
    for i in range(1, len(polygon)):
        dx = polygon[i][0] - polygon[i-1][0]
        dy = polygon[i][1] - polygon[i-1][1]
        cnt += math.gcd(abs(dx), abs(dy))
    return cnt

def count_inside_points(polygon):
    """ pick's theorem """
    A = surface(polygon)
    return round(A - count_perimeter_length(polygon) / 2 + 1)

print(count_inside_points(nodes) + count_perimeter_length(nodes))
