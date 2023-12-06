import sys


with open('./data/06-1/input', 'r') as input_file:
    inp = input_file.readlines()
    inp = [line for line in inp if len(line.strip())]

"""
with open('./test/input', 'r') as input_file:
    inp = input_file.readlines()
"""

times = [int(i.strip()) for i in inp[0].split(':')[1].strip().split()]
records = [int(i.strip()) for i in inp[1].split(':')[1].strip().split()]

ans = 1

for i, times in enumerate(times):
    cur_record = records[i]
    best_solutions = 0
    for hold_time in range(times):
        cur_speed = hold_time
        d_traveled = hold_time * (times - hold_time)
        if d_traveled > cur_record:
            best_solutions += 1
    ans *= best_solutions

print(ans)
