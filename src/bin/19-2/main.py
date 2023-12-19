from collections import OrderedDict
import pprint
import re
import sys
from typing import Any

TEST = False
if TEST:
    fp = './test/input_19'
else:
    fp = './data/19/input'


with open(fp, 'r') as inputfile:
    raw = inputfile.readlines()


ALL_SEPARATORS = ['<', '>', ':']
def parse_rule(rule):
    if not any([sep in rule for sep in ALL_SEPARATORS]):
        field = None
        comp = None
        target_value = -1
        destination = rule
    else:
        field, target_value, destination = re.split('|'.join(ALL_SEPARATORS), rule)
        comp = rule[len(field)]
        # if comp == '<':
        #     cond = lambda i: i < int(target_value)
        # elif comp == '>':
        #     cond = lambda i: i > int(target_value)
    return field, comp, int(target_value), destination


def parse_workflow(line):
    spl = line.strip().split('{')
    name, contents = spl[0], spl[1][:-1]
    rules_str = contents.split(',')
    rules = [parse_rule(i) for i in rules_str]
    return name, rules


workflows = OrderedDict()
i = 0
line = raw[0]
while len(line.strip()):
    name, rules = parse_workflow(line)
    workflows[name] = rules
    i += 1
    line = raw[i]

x = (1, 4000)
m = (1, 4000)
a = (1, 4000)
s = (1, 4000)

cur_pos = 'in'
# path item is (workflow_name, current_rule_index, [x, m, a, s])
paths = [(cur_pos, 0, [x, m, a, s])]

field_map = 'xmas'
while not all(i[0] in ('A', 'R') for i in paths):
    processed_paths = []
    for path in paths:
        wf_name, rule_idx, path_fields = path
        if wf_name in ('A', 'R'):
            processed_paths.append(path)
            continue

        field, comp, target_val, destination = workflows[wf_name][rule_idx]
        if not field and destination:
            processed_paths.append((destination, 0, path_fields))
            continue
        else:
            field_index = field_map.index(field)
            field = path_fields[field_index]
            if comp == '>':
                if target_val < field[0]:
                    processed_paths.append(destination, 0, path_fields)
                    continue
                elif target_val > field[1]:
                    continue
                redirected_range = (target_val + 1, field[1])
                continuing_range = (field[0], target_val)

                # build the successful/redirected path item
                redirected_path_fields = path_fields.copy()
                redirected_path_fields[field_index] = redirected_range
                redirected_path = (destination, 0, redirected_path_fields)
                processed_paths.append(redirected_path)

                # add a new split path for the path that does not respect the criteria and continues on the same workflow
                continuing_path_fields = path_fields.copy()
                continuing_path_fields[field_index] = continuing_range
                continuing_path = (wf_name, rule_idx+1, continuing_path_fields)
                processed_paths.append(continuing_path)
            else:
                if target_val > field[1]:
                    processed_paths.append(destination, 0, path_fields)
                    continue
                elif target_val < field[0]:
                    continue
                continuing_range = (target_val, field[1])
                redirected_range = (field[0], target_val - 1)

                # build the successful/redirected path item
                redirected_path_fields = path_fields.copy()
                redirected_path_fields[field_index] = redirected_range
                redirected_path = (destination, 0, redirected_path_fields)
                processed_paths.append(redirected_path)

                # add a new split path for the path that does not respect the criteria and continues on the same workflow
                continuing_path_fields = path_fields.copy()
                continuing_path_fields[field_index] = continuing_range
                continuing_path = (wf_name, rule_idx+1, continuing_path_fields)
                processed_paths.append(continuing_path)

    paths = processed_paths

final_paths = [item for item in paths if item[0] == 'A']

total = 0
for p in final_paths:
    ranges = p[2]
    comb = 1
    for rng in ranges:
        comb = comb * (rng[1] - rng[0] + 1)
    total += comb
print(total)
