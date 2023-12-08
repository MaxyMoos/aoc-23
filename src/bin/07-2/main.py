from collections import Counter
from enum import IntEnum


with open('./data/07-1/input', 'r') as input_file:
    inp = input_file.readlines()
    inp = [line for line in inp if len(line.strip())]


hands_list = []
for line in inp:
    h,b = line.split(' ')
    hands_list.append((h,int(b.strip())))


CARD_STR = 'J23456789TQKA'


class Types(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OAK = 4
    FULL = 5
    FOUR_OAK = 6
    FIVE_OAK = 7


def _compute_type(chars):
    strength = 0
    if 'J' in chars:
        for jcard in CARD_STR[1:]:
            strength = max(strength, _compute_type(chars.replace('J', jcard)))
            if strength == Types.FIVE_OAK:
                break
        return strength
    else:
        counter = Counter(chars)
        stats = sorted(counter.most_common(), key=lambda i: (i[1], CARD_STR.index(i[0])), reverse=True)
        ordered = ''.join([i[0] * i[1] for i in stats])

        if stats[0][1] == 5:
            return Types.FIVE_OAK
        if stats[0][1] == 4:
            return Types.FOUR_OAK
        elif stats[0][1] == 3:
            if stats[1][1] == 2:
                return Types.FULL
            else:
                return Types.THREE_OAK
        elif stats[0][1] == 2:
            if stats[1][1] == 2:
                return Types.TWO_PAIR
            else:
                return Types.ONE_PAIR
        return Types.HIGH_CARD


class Hand():
    def __repr__(self) -> str:
        return self.chars

    def __init__(self, chars):
        self.chars = chars
        self.type = _compute_type(self.chars)

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
    ret += (i+1) * item[1]
print(ret)
