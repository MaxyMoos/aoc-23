import copy
import sys
import time


TEST = False
if TEST:
    fp = './test/input'
else:
    fp = './data/16/input'

with open(fp, 'r') as inputfile:
    inp = [i.strip() for i in inputfile if len(i.strip())]

def pretty(m):
    print('\n'.join(i for i in m))


class Beam:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def __eq__(self, __value: object) -> bool:
        return self.pos == __value.pos and self.direction == __value.direction

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def move(self):
        self.pos = (self.x + self.direction[0], self.y + self.direction[1])

    def __repr__(self) -> str:
        return f"<{self.pos}|{self.direction}>"


class Beams:
    def __init__(self, m: list[list[str]], beams: list[Beam] = None):
        self.map = m
        if beams is not None:
            self.beams = beams
        else:
            self.beams = []
        self.history = set()
        self.energized = [i.pos for i in self.beams]

    def move(self):
        new_beams = []
        for beam in self.beams:
            match self.map[beam.x][beam.y]:
                case '.':
                    beam.move()
                case '-':
                    if beam.direction[1] in (-1, 1):
                        beam.move()
                    else:
                        new_beams.append(Beam((beam.x, beam.y + 1), (0, 1)))
                        beam.pos = (beam.x, beam.y - 1)
                        beam.direction = (0, -1)
                case '|':
                    if beam.direction[1] in (-1, 1):
                        new_beams.append(Beam((beam.x + 1, beam.y), (1, 0)))
                        beam.pos = (beam.x - 1, beam.y)
                        beam.direction = (-1, 0)
                    else:
                        beam.move()
                case '/':
                    if beam.direction[0] in (-1, 1):
                        beam.pos = (beam.x, beam.y - beam.direction[0])
                        beam.direction = (0, -beam.direction[0])
                    elif beam.direction[1] in (-1, 1):
                        beam.pos = (beam.x - beam.direction[1], beam.y)
                        beam.direction = (-beam.direction[1], 0)
                case '\\':
                    if beam.direction[0] in (-1, 1):
                        beam.pos = (beam.x, beam.y + beam.direction[0])
                        beam.direction = (0, beam.direction[0])
                    elif beam.direction[1] in (-1, 1):
                        beam.pos = (beam.x + beam.direction[1], beam.y)
                        beam.direction = (beam.direction[1], 0)
        self.beams += new_beams

    def compute_history(self):
        for b in self.beams:
            self.history.add((b.pos, b.direction))

    def compute_energized(self):
        for beam in self.beams:
            if not beam.pos in self.energized:
                self.energized.append(beam.pos)

    def clean(self):
        clean_beams = []
        for beam in self.beams:
            if beam.x < 0 or beam.x > len(self.map) - 1 or beam.y < 0 or beam.y > len(self.map[0]) - 1:
                continue
            if (beam.pos, beam.direction) in self.history:
                continue
            clean_beams.append(beam)
        self.beams = clean_beams

b = Beams(inp, ([Beam((0, 0), (0, 1))]))
history = [(0, 0)]
while len(b.beams):
    b.move()
    b.clean()
    b.compute_history()
    b.compute_energized()

print(len(b.energized))
