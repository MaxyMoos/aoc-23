import sys


TEST = False
fp = './data/15/input'
if TEST:
    fp = './test/input'

with open(fp, 'r') as inp_f:
    inp = [i.strip() for i in inp_f.readlines() if len(i.strip())]


boxes = {i: [] for i in range(256)}


def run_hash(s):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val = val % 256
    return val


def parse_item(s):
    if '-' in s:
        lens_label = s.split('-')[0]
        box_id = run_hash(lens_label)
        remove = False
        for item in boxes[box_id]:
            if item[0] == lens_label:
                remove = True
                break
        if remove:
            boxes[box_id].remove(item)
    elif '=' in s:
        lens_label, focus = s.split('=')
        box_id = run_hash(lens_label)
        replaced = False
        for i, item in enumerate(boxes[box_id]):
            if item[0] == lens_label:
                boxes[box_id][i] = (lens_label, int(focus))
                replaced = True
                break
        if not replaced:
            boxes[box_id].append((lens_label, int(focus)))


inp = inp[0]
inp = inp.replace('\n', '')
inp = inp.split(',')

total = 0
for item in inp:
    parse_item(item)

for k, v in boxes.items():
    if len(v) == 0:
        continue
    for i, item in enumerate(v):
        total += (k+1) * (i+1) * item[1]
print(total)
