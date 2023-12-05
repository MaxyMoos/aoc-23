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
        for seed_idx, seed_struct in enumerate(seed_ranges):
            seed_table, seed_start, seed_end = seed_struct[0], seed_struct[1], seed_struct[2]
            if seed_table != table:
                seed_ranges[seed_idx] = (table, seed_start, seed_end)
        table += 1
        continue

    dest_start, src_start, src_len = map(int, line.split(' '))
    for seed_range_idx, seed_range in enumerate(seed_ranges):
        cur_seed_table, range_start, range_end = seed_range[0], seed_range[1], seed_range[2]
        if cur_seed_table == table:
            continue

        if range_start <= src_start + src_len and range_end >= src_start:
            # we intersect the current table range
            if range_start >= src_start and range_end <= src_start + src_len:
                # seed range is fully contained: just transform the range
                seed_ranges[seed_range_idx] = (table, dest_start + range_start - src_start, dest_start + range_end - src_start)
            else:
                new_ranges = [
                    (min(range_start, src_start), max(range_start, src_start) - 1),
                    (max(range_start, src_start), min(range_end, src_start + src_len)),
                    (min(range_end, src_start + src_len) + 1, max(range_end, src_start + src_len))
                ]
                if new_ranges[0][1] == range_start - 1:
                    new_ranges = new_ranges[1:]
                if new_ranges[-1][0] == range_end + 1:
                    new_ranges = new_ranges[:-1]

                # print(f"Range {range_start, range_end} intersects table at {src_start, src_start + src_len}. Splitting into {new_ranges}")
                if new_ranges[0][0] < src_start:
                    seed_ranges[seed_range_idx] = (
                        cur_seed_table + 1,
                        new_ranges[0][0],
                        new_ranges[0][1]
                    )
                else:
                    seed_ranges[seed_range_idx] = (
                        cur_seed_table + 1,
                        dest_start + new_ranges[0][0] - src_start,
                        dest_start + new_ranges[0][1] - src_start,
                    )

                for i, nr in enumerate(new_ranges[1:]):
                    seed_ranges.insert(seed_range_idx + i + 1, (cur_seed_table, nr[0], nr[1]))
        else:
            pass

the_min = min([i[1] for i in seed_ranges])
print(f"{the_min}")
