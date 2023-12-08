from collections import Counter
from enum import IntEnum
import sys
from typing import Any


with open('./data/07-1/input', 'r') as input_file:
    inp = input_file.readlines()
    inp = [line for line in inp if len(line.strip())]

"""with open('./test/input') as input_file:
    inp = input_file.readlines()
    inp = [line for line in inp if len(line.strip())]
"""
hands_list = []
for line in inp:
    h,b = line.split(' ')
    hands_list.append((h,int(b.strip())))


CARD_STR = '23456789TJQKA'


class Hand():
    class Types(IntEnum):
        HIGH_CARD = 1
        ONE_PAIR = 2
        TWO_PAIR = 3
        THREE_OAK = 4
        FULL = 5
        FOUR_OAK = 6
        FIVE_OAK = 7

    def __repr__(self) -> str:
        return self.chars

    def __init__(self, chars):
        self.chars = chars
        self.type = self._compute_type()

    def _compute_type(self) -> Types:
        counter = Counter(self.chars)
        self.stats = sorted(counter.most_common(), key=lambda i: (i[1], CARD_STR.index(i[0])), reverse=True)
        self.ordered = ''.join([i[0] * i[1] for i in self.stats])

        if self.stats[0][1] == 5:
            return self.Types.FIVE_OAK
        if self.stats[0][1] == 4:
            return self.Types.FOUR_OAK
        elif self.stats[0][1] == 3:
            if self.stats[1][1] == 2:
                return self.Types.FULL
            else:
                return self.Types.THREE_OAK
        elif self.stats[0][1] == 2:
            if self.stats[1][1] == 2:
                return self.Types.TWO_PAIR
            else:
                return self.Types.ONE_PAIR
        return self.Types.HIGH_CARD

    def __gt__(self, other):
        if self.type != other.type:
            return self.type > other.type

        for i, c in enumerate(self.chars):
            a = CARD_STR.index(self.chars[i])
            b = CARD_STR.index(other.chars[i])
            if a != b:
                return a > b
        return False


sorted_hands = sorted(hands_list, key=lambda i: Hand(i[0]))
ret = 0
for i, item in enumerate(sorted_hands):
    print(item)
    #print(f"Hand {Hand(item[0]).stats} ({Hand(item[0]).type}) has rank {i+1} so gets ({i+1} * {item[1]} = {(i+1) * item[1]} as score)")
    ret += (i+1) * item[1]
print(ret)
