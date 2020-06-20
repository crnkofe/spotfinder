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
    print(cars_and_spots)

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




print("\n".join(fill_lot(map, 25)))
