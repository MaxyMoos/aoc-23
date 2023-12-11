from itertools import combinations
from pprint import pprint
import sys


with open('./data/11-1/input', 'r') as input_file:
    inp = input_file.readlines()
    inp = [[c for c in line.strip()] for line in inp if len(line.strip())]

max_gal = sum([i.count('#') for i in inp])
galaxy_map = {}

x_offset = 0  # nombre de lignes ajoutées
non_empty_cols = set()
galaxies = []

global_offset = 2

for i, line in enumerate(inp):
    if not '#' in line:
        x_offset += (global_offset - 1)
        continue
    else:
        for j, char in enumerate(line):
            if char == "#":
                galaxies.append((i + x_offset, j))
                non_empty_cols.add(j)
empty_cols = [i for i in range(len(inp[0])) if i not in non_empty_cols]

for i, item in enumerate(galaxies):
    galaxies[i] = (item[0], item[1] + (global_offset - 1) * len([1 for col in empty_cols if col < item[1]]))

galaxy_pairs = list(combinations([i for i in range(max_gal)], 2))

distance_map = {}
for src, dest in galaxy_pairs:
    key = (src, dest)
    src_coords = galaxies[src]
    dest_coords = galaxies[dest]
    distance_map[key] = abs(dest_coords[0] - src_coords[0]) + abs(dest_coords[1] - src_coords[1])

print(sum(distance_map.values()))
