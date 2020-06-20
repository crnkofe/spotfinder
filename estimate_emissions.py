#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a partial transcript of EURO standard emissions from
   https://www.rac.co.uk/drive/advice/emissions/euro-emissions-standards/

   Also some function to calculate and display emissions given a set of parameters:
   -
"""

import json
import random
from matplotlib import pyplot as plt
import numpy as np
import math #needed for definition of pi


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
car = "opel_corsa_14"
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


def calculate_emissions(distance, emission_limits, co2_limit):
    return {
        "CO_total": distance * emission_limits.get("CO", 0), # g
        "THC_total": distance * emission_limits.get("THC", 0),  # g
        "NMHC_total": distance * emission_limits.get("NMHC", 0), # g
        "NOx_total": distance * emission_limits.get("NOx", 0),
        "CO2_total": distance * co2_limit
    }


minimal_emissions_per_day = []
emissions_per_day = []

total_laps = 0
total_lap_length = 0
for day in range(count_days):
    total_laps += simulate_laps(bullseye_probability, cutoff)
    current_lap_length = total_laps * lap_length
    # for minimal emissions assume driver takes at most one lap
    # to find a free parking spot using the spotfinder
    minimal_emissions_per_day.append(calculate_emissions(
        day * lap_length,
        emission_limits.get(standard, {}),
        car_co2_emmissions.get(car, 0)))
    emissions_per_day.append(calculate_emissions(
        current_lap_length,
        emission_limits.get(standard, {}),
        car_co2_emmissions.get(car, 0)))

total_lap_length = total_laps * lap_length

print("Total laps: {}".format(total_laps))
print("Distance driven: {ln:.2f} km".format(ln=total_lap_length))
total_emissions = json.dumps(
    calculate_emissions(total_lap_length,
                        emission_limits.get(standard, {}),
                        car_co2_emmissions.get(car, 0)),
    )
print("Total emissions: {}".format(total_emissions))

x = np.arange(0, count_days, 1)
y = np.array(list(map(lambda x: x.get("CO2_total", 0) / 1e3, emissions_per_day)))
plt.plot(x, y, label="CO2 no-action estimate")

y_min = np.array(list(map(lambda x: x.get("CO2_total", 0) / 1e3, minimal_emissions_per_day)))
plt.plot(x, y_min, label="CO2 spotfinder estimate")

plt.xlabel("day")
plt.ylabel("CO2 [kg]")

plt.title('CO2 emissions savings estimate')
plt.show()
