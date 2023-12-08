import sys


with open('./data/08-1/input', 'r') as input_file:
    inp = input_file.readlines()
    inp = [line.strip() for line in inp if len(line.strip())]

directions = inp[0]

dirmap = {
    l[0:3]: [l[7:10], l[12:15]] for l in inp[1:]
}

curpos = 'AAA'
dir_index = 0
while curpos != 'ZZZ':
    i = 0
    if directions[dir_index % len(directions)] == 'R':
        i = 1
    curpos = dirmap[curpos][i]
    dir_index += 1
    dir_index = dir_index

print(dir_index)
sys.exit(0)
