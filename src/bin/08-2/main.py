import math
import sys


with open('./data/08-1/input', 'r') as input_file:
    inp = input_file.readlines()
    inp = [line.strip() for line in inp if len(line.strip())]


directions = inp[0]
dirmap = {l[0:3]: [l[7:10], l[12:15]] for l in inp[1:]}
curpos = [k for k in dirmap.keys() if k.endswith('A')]
dir_index = 0

while not len(list(filter(lambda i: isinstance(i, int), curpos))) == len(curpos):
    i = 0
    if directions[dir_index % len(directions)] == 'R':
        i = 1
    for ind, pos in enumerate(curpos):
        if isinstance(pos, int):
            continue
        curpos[ind] = dirmap[pos][i]
        if curpos[ind].endswith('Z'):
            curpos[ind] = dir_index + 1
    dir_index += 1

print(math.lcm(*curpos))
