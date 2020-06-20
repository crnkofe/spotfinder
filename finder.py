#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sample path finding app

Takes a parking lot as input, fills it up at random with cars, then uses
random starting position and finds the nearest parking spot.

Generates directions for each car

Legend:
    o - impassable terrain
    s - starting point (entry to and exit from parking lot)
    # - free parking spot
    c - car
    - - passable road
"""

import sys
import random


if len(sys.argv) != 2:
    print("Usage: python finder.py micro_lot.txt")
    sys.exit(1)


movement_map = {
    (0, 1): "right",
    (0, -1): "left",
    (1, 0): "down",
    (-1, 0):  "up"
}


with open(sys.argv[1]) as map_file:
    map = [line.strip() for line in map_file]


def fill_lot(map, count_cars):
    total_spots = 0
    for row in map:
        total_spots += len([el for el in row if el == '#'])

    cars_and_spots = []
    for i in range(total_spots):
        if i < count_cars:
            cars_and_spots.append('c')
        else:
            cars_and_spots.append('#')

    random.shuffle(cars_and_spots)

    current_index = 0
    new_map = []

    for row in map:
        new_row = []
        for c in row:
            if c == '#':
                new_row.append(cars_and_spots[current_index])
                current_index += 1
            else:
                new_row.append(c)
        new_map.append("".join(new_row))
    return new_map


def select_starting_point(map):
    """Return at random one possible starting point [row_index, column_index]
    """
    starting_points = []
    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col == 's':
                starting_points.append([row_idx, col_idx])
    return random.choice(starting_points)


def is_valid(loc, map):
    if loc[0] < 0:
        return False
    if loc[1] < 0:
        return False
    if loc[0] >= len(map):
        return False
    row_length = max([len(x) for x in map])
    if loc[1] >= row_length:
        return False
    if map[loc[0]][loc[1]] not in ('-', 's', '#'):
        return False
    return True


def find_neighbours(loc, map):
    # technically we could also go diagonally but this is simpler
    options = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    possible_neighbours = [[x + y for x, y in zip(loc, option)] for option in options]
    return [position for position in possible_neighbours if is_valid(position, map)]


def breadth_first_search(start_loc, map):
    queue = [start_loc]
    visited = set(tuple(start_loc))
    parents = {}
    while queue != []:
        loc = queue.pop(0)
        if map[loc[0]][loc[1]] == '#':
            return loc, parents
        for neighbour in find_neighbours(loc, map):
            if tuple(neighbour) not in visited:
                visited.add(tuple(neighbour))
                parents[tuple(neighbour)] = tuple(loc)
                queue.append(neighbour)
    return None, {}


def trace_path(start_loc, end, parent):
    path = []
    while tuple(end) != tuple(start_loc):
        path.insert(0, end)
        end = parents[tuple(end)]
    return [start_loc] + path


def instructions(path):
    movements = []
    previous = path[0]
    next = list(path[1])
    direction = [x - y for x, y in zip(next, previous)]
    steps = 1
    for loc in path[2:]:
        new_direction = [x - y for x, y in zip(list(loc), next)]
        if tuple(new_direction) != tuple(direction):
            movements.append({
                "move": movement_map[tuple(direction)],
                "steps": steps
            })
            direction = new_direction
            steps = 1
        else:
            steps += 1
        previous = next
        next = loc

    movements.append({
        "move": movement_map[tuple(direction)],
        "steps": steps
    })
    return movements


lot = fill_lot(map, 35)

start_loc = select_starting_point(lot)
parking_loc, parents = breadth_first_search(start_loc, lot)
path = trace_path(start_loc, parking_loc, parents)

print("\n".join(lot))

for p in path:
    s = lot[p[0]]
    split_c = [c for c in s]
    split_c[p[1]] = 'x'
    lot[p[0]] = "".join(split_c)

print("\n")
print("\n".join(lot))


print(instructions(path))
