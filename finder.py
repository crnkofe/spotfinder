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


if len(sys.argv) != 2:
    print("Usage: python finder.py micro_lot.txt")
    sys.exit(1)

print(sys.argv)
with open(sys.argv[1]) as map_file:
    map = [line.strip() for line in map_file]

print(map)
