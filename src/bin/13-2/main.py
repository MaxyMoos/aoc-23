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


def hdistance(line1, line2):
    glob_distance = sum([1 for el1, el2 in itertools.zip_longest(line1, line2) if el1 != el2])
    if glob_distance == 1:
        for i in range(len(line1)):
            if line1[i] != line2[i]:
                break
        return glob_distance, i
    return glob_distance, -1


def get_modified_patterns(pattern):
    new_patterns = []
    # 1. check neighbor lines that differ by 1 char
    for i in range(1, len(pattern)):
        dist, index = hdistance(pattern[i], pattern[i-1])
        if dist == 1:
            new_pattern = pattern.copy()
            new_pattern[i] = pattern[i][:index] + pattern[i-1][index] + pattern[i][index+1:]
            new_patterns.append(new_pattern)

    # 2. check existing symmetries' borders to see if they differ by 1 char
    for sym in get_line_sym(pattern):
        if is_perfect(pattern, sym):
            continue
        sym_size = get_sym_size(pattern, sym)
        dist, index = hdistance(pattern[sym-sym_size-1], pattern[sym+sym_size])
        if dist == 1:
            new_pattern = pattern.copy()
            new_pattern[sym-sym_size-1] = pattern[sym-sym_size-1][:index] + pattern[sym+sym_size][index] + pattern[sym-sym_size-1][index+1:]
            new_patterns.append(new_pattern)

    return new_patterns


def process_pattern(pattern, exclude_hsyms=None, exclude_vsyms=None):
    htotal, vtotal = 0, 0

    hsyms = get_line_sym(pattern)
    tpattern = transpose_pattern(pattern)
    vsyms = get_line_sym(tpattern)

    perfect_hsyms = list(filter(lambda a: is_perfect(pattern, a), hsyms))
    perfect_vsyms = list(filter(lambda a: is_perfect(tpattern, a), vsyms))

    if exclude_hsyms is not None:
        perfect_hsyms = [item for item in perfect_hsyms if item not in exclude_hsyms]
    if exclude_vsyms is not None:
        perfect_vsyms = [item for item in perfect_vsyms if item not in exclude_vsyms]

    if len(perfect_hsyms) == 1:
        htotal += perfect_hsyms[0]
    elif len(perfect_vsyms) == 1:
        vtotal += perfect_vsyms[0]

    return htotal, vtotal


if __name__ == '__main__':
    patterns = get_patterns(inp)
    htotal, vtotal = 0, 0
    for i, pattern in enumerate(patterns):
        original_hsyms = [i for i in get_line_sym(pattern) if is_perfect(pattern, i)]
        original_vsyms = [i for i in get_line_sym(transpose_pattern(pattern)) if is_perfect(transpose_pattern(pattern), i)]

        alt_patterns = get_modified_patterns(pattern)
        alt_patterns += [transpose_pattern(i) for i in get_modified_patterns(transpose_pattern(pattern))]
        for alt_pattern in alt_patterns:
            alt_h, alt_v = process_pattern(alt_pattern, original_hsyms, original_vsyms)
            if alt_h > 0:
                htotal += alt_h
                break
            elif alt_v > 0:
                vtotal += alt_v
                break

    print(vtotal + 100 * htotal)
