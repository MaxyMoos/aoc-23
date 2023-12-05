import string

with open('./data/03-1/input', 'r') as input_file:
    input = input_file.read()

arr = input.split('\n')
arr = [i for i in arr if len(i)]
x_max = len(arr[0]) - 1
y_max = len(arr) - 1


class Symbol():
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char

    def get_neighbors(self):
        ret = []
        for ycoord in (self.y - 1, self.y + 1):
            if ycoord < 0 or ycoord > y_max:
                continue
            for xcoord in range(self.x - 1, self.x + 1 + 1):
                if xcoord < 0 or xcoord > x_max:
                    continue
                else:
                    ret.append((xcoord, ycoord))
        if self.x != 0:
            ret.append((self.x - 1, self.y))
        if self.x + 1 + 1 <= x_max:
            ret.append((self.x + 1, self.y))
        return ret

    def __repr__(self) -> str:
        return f"<({self.x}, {self.y}) \"{self.char}\">"


class Number():
    def __init__(self, x, y) -> None:
        x_init = x
        self.y = y
        while (x - 1 >= 0 and arr[y][x - 1].isdigit()):
            x = x - 1
        self.x = x
        while (x_init + 1 <= x_max and arr[y][x_init + 1].isdigit()):
            x_init += 1
        self.str = arr[y][self.x:x_init + 1]

    def __repr__(self) -> str:
        return f"\"{self.str}\" {self.x, self.y}"

    def __eq__(self, __value: object) -> bool:
        return (
            self.x == __value.x
            and self.y == __value.y
            and self.str == __value.str
        )

    def __hash__(self) -> int:
        return hash(f"{self.x}{self.y}{self.str}")

sum = 0
for y, line in enumerate(arr):
    for x, char in enumerate(line):
        if char == '*':
            number_neighbors = []
            for coords in Symbol(x, y, char).get_neighbors():
                if arr[coords[1]][coords[0]].isdigit():
                    number_neighbors.append(Number(coords[0], coords[1]))
            if len(set(number_neighbors)) > 1:
                partial = 1
                for elem in set(number_neighbors):
                    partial *= int(elem.str)
                print(f"{Symbol(x,y,char)} neighbors set: {set(number_neighbors)}.\n\tpartial = {partial}")
                sum += partial
print(sum)
