import collections
import itertools
import sys

from pprint import pprint

TEST = False

if TEST:
    fp = './test/input'
else:
    fp = './data/12-1/input'


with open(fp, 'r') as input_file:
    inp = [i.strip() for i in input_file.readlines() if len(i)]


def is_correct(springs_str: str, groups: list[int]) -> bool:
    """ Checks validity of a springs string vs a group of ints """
    split = [i for i in springs_str.split('.') if len(i)]
    return (
        len(split) == len(groups)
        and all([len([j for j in item if j == '#']) == groups[i] for i, item in enumerate(split)])
    )


def get_valid_combinations(s: str, groups: list[int]) -> int:
    for char in s:
        if char == '?':
            opt_1 = s.replace('?', '#', 1)  # replace first occurrence
            opt_2 = s.replace('?', '.', 1)
            return (
                get_valid_combinations(opt_1, groups)
                + get_valid_combinations(opt_2, groups)
            )
    if not '?' in s:
        return 1 if is_correct(s, groups) else 0


total = 0
for line in inp:
    springs, groups = line.split(' ')
    groups = list(map(int, groups.split(',')))
    combs = get_valid_combinations(springs, groups)
    print(f"{springs} / {groups} => combinations = {combs}")
    total += combs
print(total)
