# Define neighbourhoods
# scores out of 10: drive, bus, bike, walk; convenience, speed, affordability, sustainability

import agentclass_JF
from neighbourhoodclass import Neighbourhood

population = agentclass_JF.populate_Austin(20)

west = Neighbourhood(1200,[[7, 7, 3, 3], [5, 5, 10, 8], [4, 5, 5, 9], [3, 3, 10, 10]], 1)

north = Neighbourhood(1000, [[7, 7, 3, 3], [6, 5, 10, 8], [4, 5, 5, 9], [2, 2, 10, 10]], 2)

riverside = Neighbourhood(900, [[7, 7, 3, 3], [4, 4, 10, 8], [3, 3, 5, 9], [1, 1, 10, 10]], 3)

all_neighbourhoods = [west, north, riverside]

for neighbourhood in all_neighbourhoods:
    neighbourhood.define_residents(population)
    neighbourhood.housing_supply = len(neighbourhood.resident_list)

