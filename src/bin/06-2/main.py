import sys


with open('./data/06-1/input', 'r') as input_file:
    inp = input_file.readlines()
    inp = [line for line in inp if len(line.strip())]

"""
with open('./test/input', 'r') as input_file:
    inp = input_file.readlines()
"""

time = 40709879
record = 215105121471005

best_solutions = 0
for hold_time in range(time):
    cur_speed = hold_time
    d_traveled = hold_time * (time - hold_time)
    if d_traveled > record:
        best_solutions += 1

print(best_solutions)
