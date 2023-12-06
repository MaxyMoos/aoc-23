import string

with open('./data/03-1/input', 'r') as input_file:
    input = input_file.read()

# with open('./test/input', 'r') as input_file:
#     input = input_file.read()

arr = input.split('\n')
arr = [item for item in arr if len(item)]
x_max = len(arr[0]) - 1
y_max = len(arr) - 1


class Number():
    def __init__(self, x, y, char):
        self.string = char
        self.x_start = x
        self.y = y

    def get_neighbors(self):
        ret = []
        for ycoord in (self.y - 1, self.y + 1):
            if ycoord < 0 or ycoord > y_max:
                continue
            for xcoord in range(self.x_start - 1, self.x_start + len(self.string) + 1):
                if xcoord < 0 or xcoord > x_max:
                    continue
                else:
                    ret.append((xcoord, ycoord))
        if self.x_start != 0:
            ret.append((self.x_start - 1, self.y))
        if self.x_start + len(self.string) + 1 <= x_max:
            ret.append((self.x_start + len(self.string), self.y))
        return ret

    def __repr__(self):
        return f"<({self.x_start}, {self.y}) \"{self.string}\">"


cur_string = ""
numbers = []
for y, line in enumerate(input.split('\n')):
    for x, char in enumerate(line):
        if char.isdigit():
            if not len(cur_string):
                cur_string = char
                start_x = x
            else:
                cur_string += char
        else:
            if len(cur_string):
                numbers.append(Number(start_x, y, cur_string))
                cur_string = ""
        if x == x_max and len(cur_string):
            numbers.append(Number(start_x, y, cur_string))
            cur_string = ""

part_numbers = []
for item in numbers:
    for coords in item.get_neighbors():
        if arr[coords[1]][coords[0]] not in (string.digits + '.'):
            part_numbers.append(int(item.string))

print(sum(part_numbers))
