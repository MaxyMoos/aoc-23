with open('./data/05-1/input', 'r') as input_file:
    inp = input_file.readlines()

seeds = [(0, int(i.strip())) for i in inp[0].split(': ')[1].split(' ')]
table = 1
for line_idx, line in enumerate(inp[3:]):
    line = line.strip()
    if len(line) == 0:
        continue

    if line.endswith('map:'):
        for seed_idx, seed_struct in enumerate(seeds):
            seed_table, seed = seed_struct[0], seed_struct[1]
            if seed_table != table:
                seeds[seed_idx] = (table, seed)
        table += 1
        continue

    dest, src, src_range = map(int, line.split(' '))
    for seed_idx, seed_struct in enumerate(seeds):
        seed_table, seed = seed_struct[0], seed_struct[1]

        if seed_table == table:
            continue

        if seed >= src and seed <= src + src_range - 1:
            diff = seed - src
            seeds[seed_idx] = (table, dest+diff)

the_min = min([i[1] for i in seeds])
print(f"{the_min}")
