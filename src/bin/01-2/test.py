import string as string_utils


with open("./data/01-1/input", "r") as input_file:
    input = input_file.read()

# with open("./test/input", "r") as input_file:
#     input = input_file.read()


AS_CHARS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


class Candidate:
    __slots__ = ["string", "index"]

    def __init__(self, string) -> None:
        self.string = string
        self.index = 0

    def getnext(self):
        return self.string[self.index + 1]

    def is_matched(self):
        return self.index == len(self.string) - 1


sum = 0
candidates = []
clean_before = False
clean_after = False
partial_sums = []

for line in input.split("\n"):
    if len(line) == 0:
        continue

    #print("line: {}".format(line))
    start = None
    end = None
    for char in line:
        to_drop = []

        if char in string_utils.digits:
            if start is None:
                start = int(char)
                clean_after = True
            else:
                end = int(char)

        for candidate in candidates:
            if char == candidate.getnext():
                candidate.index += 1
            else:
                to_drop.insert(0, candidates.index(candidate))
            if candidate.is_matched():
                if start is None:
                    start = AS_CHARS.index(candidate.string) + 1
                    clean_after = True
                else:
                    end = AS_CHARS.index(candidate.string) + 1
                    clean_before = True

        if clean_before:
            candidates = []
            to_drop = []
            clean_before = False

        for item in to_drop:
            candidates.pop(item)
        to_drop = []

        for elem in AS_CHARS:
            if char == elem[0]:
                candidates.append(Candidate(elem))

        if clean_after is True:
            candidates = []
            clean_after = False

    if end is None:
        end = start

    #print(f"start = {start}, end = {end}")
    sum += int("{}{}".format(start, end))
    partial_sums.append(sum)

print(sum)
with open('python-sums.txt', 'w') as output:
    output.write("\n".join([str(item) for item in partial_sums]))
