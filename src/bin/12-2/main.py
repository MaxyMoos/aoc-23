import collections
import functools
import itertools
import sys

from pprint import pprint

TEST = True

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


@functools.lru_cache(maxsize=None)
def get_combs(group, count):
    cur_count = count[0]

    total = 0

    hs_pos = None

    for idx in range(len(group) - cur_count + 1):
        region = group[idx:idx + cur_count]

        # Only a valid island if it has "?" or "#"
        has_dot = "." in region

        # Over extended
        over_ext = group[idx + cur_count] == "#" if idx + cur_count < len(group) else False

        # Following a #
        prev_c = group[idx - 1] == "#" if idx > 0 else False

        if not (has_dot or over_ext or prev_c):
            if len(count) == 1:
                if "#" not in group[idx + cur_count + 1:]:
                    total += 1
            else:
                total += get_combs(group[idx + cur_count + 1:], count[1:])

        if hs_pos is not None and hs_pos < idx:
            break

        if hs_pos is None and "#" in region:
            hs_pos = idx + region.index("#")

    return total


total = 0
for line in inp[0:1]:
    springs, groups = line.split(' ')
    springs = '?'.join([springs] * 5)
    groups = ','.join([groups] * 5)
    groups = tuple(map(int, groups.split(',')))
    print(f"SPRINGS: {springs}")
    import ipdb; ipdb.set_trace()
    combs = get_combs(springs, groups)
    print(f"{springs} / {groups} => combinations = {combs}")
    total += combs
print(total)
