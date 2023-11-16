# Define neighbourhoods
# scores out of 10: drive, bus, bike, walk; convenience, speed, affordability, sustainability

import agent
import neighbourhoodclass as neighbourhood 
import agent_env_monthly as aem
import matplotlib.pyplot as plt
import numpy as np

#Step 1: Initiate Population
population = 100
population_list = agent.populate_Austin(population)

#Step 2: Initiate Neighbourhoods + Step 3: Define Commute Parameters
neighbourhood_list = neighbourhood.initiate_neighbourhoods(population_list)

#Step 3b: Update Initial Satisfaction of each Resident based on Initial Neighbourhood Characteristics

for resident in population_list:
    resident.update_satisfaction(neighbourhood_list)

#Step 4: Agent-Agent Monthly Interaction


months = 100

counts = [[],[],[]]

for i in range(months):

    #4a: Compare with Random Neighbour + Switch Transit if Satisfaction is Greater
    for resident in population_list:
        resident.monthly_neighbour_interaction(neighbourhood_list)

    def unit_test_1():
        for neighbourhood in neighbourhood_list:
            print(f"neighbourhood #: {neighbourhood.neighbourhood_id}")
            for resident in neighbourhood.resident_list:
                print(f"resident # {resident.id} took {resident.transit_prev} and now takes {resident.transit}")

    #5: Monthly Agent-Environment Interaction (evaluates system performance after transit changes and updates self.commutescores descriptors for each neighbourhood)

    for neighbourhood in neighbourhood_list:
        neighbourhood.commute_scores = aem.commute_update(neighbourhood,population)

    #4b: Residents Re-evaluate Satisfaction Relative to Last Month's Commutes and Chooses to Stay or Revert Back to Previous Commute
    for resident in population_list:
        resident.update_satisfaction(neighbourhood_list)
        resident.evaluate_commute_switch()

    #print(f"Month: {i}")

    for neighbourhood in neighbourhood_list:
        neighbourhood.count_transit()
        #print(f"Neighbourhood #{neighbourhood.neighbourhood_id} has {neighbourhood.transit_counts}")
        counts[neighbourhood.neighbourhood_id].append(neighbourhood.transit_counts)

  
# for count in counts:
#     print(count)
#     print()

X = np.arange(0, months, 1)

#For West Campus
print(counts[0])
walk = [list[3] for list in counts[0]]
#print(walk)

plt.plot(X, walk, label = "west campus walk")
plt.show()
# bus = 
# bike = 
# walk = 

counts = [[],[],[]]





