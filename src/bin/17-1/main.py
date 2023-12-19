from queue import PriorityQueue
import pprint
import sys

TEST = False
if TEST:
    fp = './test/input'
else:
    fp = './data/17/input'

with open(fp, 'r') as inputfile:
    inp = inputfile.readlines()
    inp = [i.strip() for i in inp if len(i.strip())]

def pretty(m):
    print('\n'.join(i for i in m))

pretty(inp)

def modified_dijkstra(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    distances = [[[[float('infinity')] * 4 for _ in range(4)] for _ in range(cols)] for _ in range(rows)]
    predecessors = [[[[None] * 4 for _ in range(4)] for _ in range(cols)] for _ in range(rows)]
    distances[start[0]][start[1]][1][0] = 0  # Start with Up direction (arbitrary choice)
    pq = PriorityQueue()
    pq.put((0, start, 1, 0))  # distance, coordinates, last direction, consecutive moves

    while not pq.empty():
        current_distance, (row, col), last_dir, consec_moves = pq.get()
        if (row, col) == end:
            return current_distance, reconstruct_path(predecessors, end, last_dir, consec_moves)

        for dir_idx, (dr, dc) in enumerate(directions):
            # backtracking verboten
            if (dr, dc) == (-directions[last_dir][0], -directions[last_dir][1]):
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                new_consec_moves = consec_moves + 1 if dir_idx == last_dir else 1
                if new_consec_moves <= 3:
                    new_distance = current_distance + int(grid[new_row][new_col])
                    if new_distance < distances[new_row][new_col][dir_idx][new_consec_moves]:
                        distances[new_row][new_col][dir_idx][new_consec_moves] = new_distance
                        predecessors[new_row][new_col][dir_idx][new_consec_moves] = (row, col, last_dir, consec_moves)
                        pq.put((new_distance, (new_row, new_col), dir_idx, new_consec_moves))

    return []

def reconstruct_path(predecessors, end, last_dir, consec_moves):
    path = []
    current = end
    current_dir = last_dir
    current_moves = consec_moves
    while predecessors[current[0]][current[1]][current_dir][current_moves]:
        path.append(current)
        c_x, c_y, last_dir, consec_moves = predecessors[current[0]][current[1]][current_dir][current_moves]
        current = (c_x, c_y)
        current_dir = last_dir
        current_moves = consec_moves
    path.append(current)  # Add the start node
    return path[::-1]

# Usage
path = modified_dijkstra(inp, (0, 0), (len(inp) - 1, len(inp[0]) - 1))
print(path)
