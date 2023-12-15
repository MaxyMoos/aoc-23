import sys


TEST = False
fp = './data/15/input'
if TEST:
    fp = './test/input'

with open(fp, 'r') as inp_f:
    inp = [i.strip() for i in inp_f.readlines() if len(i.strip())]


def run_hash(s):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val = val % 256
    return val

inp = inp[0]
inp = inp.replace('\n', '')
inp = inp.split(',')

total = 0
for item in inp:
    total += run_hash(item)
print(total)
