with open('data/02-1/input.txt', 'r') as input_file:
    input = input_file.read()


input = input.split('\n')
good_games = []

for line in input:
    if len(line) == 0:
        continue

    game_id = int(line[4:].split(':')[0])
    bad_game = False
    sets = line.split(':')[1].split(';')
    sets = [item.strip() for item in sets]

    min_set = [0,0,0] # rgb
    for set_i, set in enumerate(sets):
        colors = set.split(',')
        for item in colors:
            duo = item.strip().split(' ')
            qty, color = duo[0], duo[1]
            if color == "red":
                if int(qty) > min_set[0]:
                    min_set[0] = int(qty)
            elif color == "green":
                if int(qty) > min_set[1]:
                    min_set[1] = int(qty)
            elif color == "blue":
                if int(qty) > min_set[2]:
                    min_set[2] = int(qty)

    power = min_set[0] * min_set[1] * min_set[2]
    good_games.append(power)

print(sum(good_games))
