#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sample path finding app

Takes a parking lot as input, fills it up at random with cars, then uses
random starting position and finds the nearest parking spot.

Generates directions for a car appearing at a starting spot.
This script will fill up the parking lot until all sports are taken

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


# this is 2d map direction which is wrong (driver at the beginning is facing
# forward
movement_map = {
    (0, 1): "right",
    (0, -1): "left",
    (1, 0): "down",
    (-1, 0):  "up"
}

clockwise_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


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
        end = parent[tuple(end)]
    return [start_loc] + path


def create_driver_instructions(path):
    movements = []
    previous = path[0]
    next = list(path[1])
    direction = [x - y for x, y in zip(next, previous)]
    steps = 1
    for loc in path[2:]:
        new_direction = [x - y for x, y in zip(list(loc), next)]
        if tuple(new_direction) != tuple(direction):
            idx_of = clockwise_directions.index(tuple(direction))
            next_idx_of = (idx_of + 1) % len(clockwise_directions)
            if tuple(new_direction) == clockwise_directions[next_idx_of]:
                turn = "right"
            else:
                turn = "left"

            movements.append({
                "move": "forward",
                "steps": steps
            })
            movements.append({
                "turn": turn,
                "steps": 0
            })
            direction = new_direction
            steps = 1
        else:
            steps += 1
        previous = next
        next = loc

    movements.append({
        "move": "forward",
        "steps": steps
    })
    return movements


def instructions_2d(path):
    movements = []
    previous = path[0]
    next = list(path[1])
    direction = [x - y for x, y in zip(next, previous)]
    steps = 1
    for loc in path[2:]:
        new_direction = [x - y for x, y in zip(list(loc), next)]
        if tuple(new_direction) != tuple(direction):
            movements.append({
                "turn": movement_map[tuple(direction)],
                "steps_forward": steps
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


def find_space_for_driver(lot):
    start_loc = select_starting_point(lot)
    parking_loc, parents = breadth_first_search(start_loc, lot)
    if parking_loc is None:
        return None, None
    path = trace_path(start_loc, parking_loc, parents)

    new_lot = [x for x in lot]

    row_idx = parking_loc[0]

    row = list(lot[row_idx])
    row[parking_loc[1]] = 'c'
    new_lot[row_idx] = "".join(row)

    lot_copy = [x for x in lot]
    for p in path:
        s = lot_copy[p[0]]
        split_c = [c for c in s]
        split_c[p[1]] = 'x'
        lot_copy[p[0]] = "".join(split_c)

    # uncomment to check entire parking lot
    # print("\n".join(lot_copy))

    return new_lot, create_driver_instructions(path)


lot = fill_lot(map, 35)
print ("Initial state\n {}".format("\n".join(lot)))

new_lot = lot
while new_lot is not None:
    new_lot, instructions = find_space_for_driver(new_lot)
    if not new_lot:
        print("Parking spot full")
    else:
        print("Instructions: {}".format(instructions))
