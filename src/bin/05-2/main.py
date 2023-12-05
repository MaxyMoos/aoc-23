import sys

with open('./data/05-1/input', 'r') as input_file:
    inp = input_file.readlines()

"""
with open('./test/input', 'r') as input_file:
    inp = input_file.readlines()
"""

seeds = [int(i.strip()) for i in inp[0].split(': ')[1].split(' ')]
tmp = []
for i, seed in enumerate(seeds[::2]):
    tmp += [(0, seed, seed + seeds[2*i + 1] - 1)]
seed_ranges = tmp

table = 1
for line_idx, line in enumerate(inp[3:]):
    line = line.strip()
    if len(line) == 0:
        continue

    if line.endswith('map:'):
        """for seed_idx, seed_struct in enumerate(seeds):
            seed_table, seed = seed_struct[0], seed_struct[1]
            if seed_table != table:
                seeds[seed_idx] = (table, seed)"""
        table += 1
        continue

    dest_start, src_start, src_len = map(int, line.split(' '))
    for seed_range_idx, seed_range in enumerate(seed_ranges):
        cur_seed_table, range_start, range_end = seed_range[0], seed_range[1], seed_range[2]
        if range_start <= src_start + src_len and range_end >= src_start:
            # we intersect the current table range
            if range_start >= src_start and range_end <= src_start + src_len:
                # seed range is fully contained: just transform the range
                seed_ranges[seed_range_idx] = (table, dest_start + range_start - src_start, dest_start + range_end - src_start)
                print(f"Range {seed_range} fully contained in table range {src_start, src_start + src_len}. As dest = {dest_start} => {seed_ranges[seed_range_idx]}")
            else:
                new_ranges = [
                    (min(range_start, src_start), max(range_start, src_start)),
                    (max(range_start, src_start), min(range_end, src_start + src_len)),
                    (min(range_end, src_start + src_len), max(range_end, src_start + src_len))
                ]
                print(f"Range {seed_range} intersects table range {src_start, src_start + src_len}, giving out:\n{new_ranges}")
                sys.exit(0)

    """
    for seed_idx, seed_struct in enumerate(seeds):
        seed_table, seed = seed_struct[0], seed_struct[1]

        if seed_table == table:
            continue

        if seed >= src and seed <= src + src_range - 1:
            diff = seed - src
            seeds[seed_idx] = (table, dest+diff)"""

the_min = min([i[1] for i in seeds])
print(f"{the_min}")
