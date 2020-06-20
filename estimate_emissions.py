#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a partial transcript of EURO standard emissions from
   https://www.rac.co.uk/drive/advice/emissions/euro-emissions-standards/

   Also some function to calculate and display emissions given a set of parameters:
   -
"""

import json
import random

emission_limits = {
    # EURO 6 (Petrol)
    "euro_6" : {
        # Implementation date (new approvals): 1 September 2014
        # Implementation date (most new registrations - see important point below table above): 1
        "CO": 1.0, #g/km
        "THC": 0.10, #g/km
        "NMHC": 0.068, #g/km
        "NOx": 0.06 #g/km
    },
    # EURO 5 (Petrol)
    "euro_5": {
        # Implementation date (new approvals): 1 September 2009
        # Implementation date (all new registrations): 1 January 2011
        "CO": 1.0, #g/km
        "THC": 0.10, #g/km
        "NMHC": 0.068, #g/km
        "NOx": 0.06, #g/km
    },
    # Euro 4 emissions standards (petrol)
    "euro_4": {
        # Implementation date (new approvals): 1 January 2005
        # Implementation date (all new registrations): 1 January 2006
        "CO": 1.0, #g/km
        "THC": 0.10, #g/km
        "NOx": 0.08 #g/km
    },
    #Euro 3 (EC2000) (Petrol)
    "euro_3": {
        #Implementation date (new approvals): 1 January 2000
        #Implementation date (all new registrations): 1 January 2001
        "CO": 2.3, #g/km
        "THC": 0.20, #g/km
        "NOx": 0.15, #g/km
    }
}


car_co2_emmissions = {
    "opel_corsa_14": 134.22 # g/km # originally 216 g/mile
}


# standard selection
standard = "euro_6"
# car selection
cars = "opel_corsa_14"
# simulate count days
count_days = 356
# count cars for which to simulate
number_of_cars = 1
# probability of finding a free parking spot in one lap
bullseye_probability = 0.3
# cutoff means at count laps we stop the simulation and assume driver found a
# place
cutoff = 5
# pick a number indicating in km how much aproximately a driver needs to
# drive in order to check all parking spots
lap_length = 1.0

random.seed()


def simulate_laps(prob, max_laps):
    for lap in range(max_laps):
        if random.random() < prob:
            return lap
    return max_laps


total_laps = 0
total_lap_length = 0
for day in range(count_days):
    total_laps += simulate_laps(bullseye_probability, cutoff)


total_lap_length = total_laps * lap_length
print("Total laps: {}".format(total_laps))
print("Distance driven: {ln:.2f} km".format(ln=total_lap_length))

