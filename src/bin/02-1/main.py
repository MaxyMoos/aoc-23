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

    for set_i, set in enumerate(sets):
        colors = set.split(',')
        for item in colors:
            duo = item.strip().split(' ')
            qty, color = duo[0], duo[1]
            if color == "red" and int(qty) > 12:
                bad_game = True
            elif color == "green" and int(qty) > 13:
                bad_game = True
            elif color == "blue" and int(qty) > 14:
                bad_game = True
        if bad_game:
            break
    if bad_game:
        continue

    good_games.append(game_id)

print(sum(good_games))
