import sys

with open('./data/05-1/input', 'r') as input_file:
    input = input_file.readlines()

seeds = [(0, int(i.strip())) for i in input[0].split(': ')[1].split(' ')]
table = 1
print(seeds)
print(f"Switching to table \"seed-to-soil\"")
for line_idx, line in enumerate(input[3:]):
    line = line.strip()
    if len(line) == 0:
        continue

    if line.endswith('map:'):
        for seed_idx, seed_struct in enumerate(seeds):
            seed_table, seed = seed_struct[0], seed_struct[1]
            if seed_table != table:
                print(f"Seed {seed} had no mapping in table. Keeping the same seed.")
                seeds[seed_idx] = (table, seed)
        print(f"Switching to table \"{line[:-5]}\"")
        table += 1
        continue

    dest, src, src_range = map(int, line.split(' '))
    for seed_idx, seed_struct in enumerate(seeds):
        seed_table, seed = seed_struct[0], seed_struct[1]

        if seed_table != table:
            continue

        if seed >= src and seed <= src + src_range - 1:
            diff = seed - src
            print(f"Seed {seed} (index {seed_idx}) has a match and is replaced by value {dest+diff}")
            seeds[seed_idx] = (seed_table + 1, dest+diff)

print(seeds)
the_min = min([i[1] for i in seeds])
print(f"{the_min} / idx = {[i[1] for i in seeds].index(the_min)}")
