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
        cond = lambda a: True
        destination = rule
    else:
        field, target_value, destination = re.split('|'.join(ALL_SEPARATORS), rule)
        comp = rule[len(field)]
        if comp == '<':
            cond = lambda i: i < int(target_value)
        elif comp == '>':
            cond = lambda i: i > int(target_value)
    return field, cond, destination


def parse_workflow(line):
    spl = line.strip().split('{')
    name, contents = spl[0], spl[1][:-1]
    rules_str = contents.split(',')
    rules = [parse_rule(i) for i in rules_str]
    return name, rules


class Input:
    def __init__(self, **kwargs):
        self._dict = {}
        for k, v in kwargs.items():
            self._dict[k] = int(v)

    def __repr__(self) -> str:
        return pprint.pformat(self._dict)

    def check_rule(self, rule):
        field, cond, destination = rule
        if field is None and destination:
            return destination

        if field not in self._dict:
            return False

        ret = cond(self._dict[field])
        if ret:
            return destination
        else:
            return False

    def get_sum(self):
        return sum(v for v in self._dict.values())


workflows = OrderedDict()
i = 0
line = raw[0]
while len(line.strip()):
    name, rules = parse_workflow(line)
    workflows[name] = rules
    i += 1
    line = raw[i]

i += 1
inputs = []
for line in raw[i:]:
    conv = dict(e.split('=') for e in line[1:-2].split(','))
    inputs.append(Input(**conv))

total = 0
for inp_line in inputs:
    first = next(iter(workflows))
    cur_pos = 'in'
    while cur_pos not in ('A', 'R'):
        cur_rules = workflows[cur_pos]
        for rule in cur_rules:
            output = inp_line.check_rule(rule)
            if not output:
                if rule == cur_rules[-1]:
                    it_wf = iter(workflows)
                    tmp = next(it_wf)
                    while tmp != cur_pos:
                        tmp = next(it_wf)
                    cur_pos = next(it_wf)  # go to next wf
                    break
                else:
                    continue
            else:
                cur_pos = output
                break
    if cur_pos == 'A':
        total += inp_line.get_sum()
print(total)
