import collections
import functools
import itertools
import sys

from pprint import pprint

TEST = False

if TEST:
    fp = './test/input'
else:
    fp = './data/13-1/input'


with open(fp, 'r') as input_file:
    inp = [i.strip() for i in input_file.readlines()]


def get_patterns(input_str):
    patterns = []
    cur_pattern = []
    for line in input_str:
        if len(line) > 0:
            cur_pattern.append(line)
        else:
            patterns.append(cur_pattern)
            cur_pattern = []
    if len(cur_pattern):
        patterns.append(cur_pattern)
    return patterns


def transpose_pattern(pattern):
    transposed = []
    for i in range(len(pattern[0])):
        transposed.append(''.join([l[i] for l in pattern]))
    return transposed


def pprint_pattern(pattern):
    for line in pattern:
        print(line)


def get_line_sym(pattern):
    sym = []
    for i in range(1, len(pattern)):
        if pattern[i] == pattern[i-1]:
            sym.append(i)
    return sym


def get_sym_size(pattern, sym_index):
    n = sym_index
    offset = 1
    while n + offset < len(pattern) and n-offset-1 >= 0 and pattern[n+offset] == pattern[n-offset-1]:
        offset += 1
    return offset


def is_perfect(pattern, sym_index):
    n = sym_index
    offset = 1
    while n + offset < len(pattern) and n-offset-1 >= 0 and pattern[n+offset] == pattern[n-offset-1]:
        offset += 1
    return n + offset == len(pattern) or n - offset - 1 < 0


if __name__ == '__main__':
    patterns = get_patterns(inp)
    htotal = 0
    vtotal = 0
    for pattern in patterns:
        hsyms = get_line_sym(pattern)
        tpattern = transpose_pattern(pattern)
        vsyms = get_line_sym(tpattern)

        perfect_hsyms = list(filter(lambda a: is_perfect(pattern, a), hsyms))
        perfect_vsyms = list(filter(lambda a: is_perfect(tpattern, a), vsyms))

        if len(perfect_hsyms) == 1 and len(perfect_vsyms) == 0:
            htotal += perfect_hsyms[0]
        elif len(perfect_vsyms) == 1 and len(perfect_hsyms) == 0:
            vtotal += perfect_vsyms[0]
        else:
            print("Issue")

    print(vtotal + 100 * htotal)
