# Define neighbourhoods
# scores out of 10: drive, bus, bike, walk; convenience, speed, affordability, sustainability

import agent
import neighbourhoodclass as neighbourhood 
import agent_env_monthly as aem
import matplotlib.pyplot as plt
import numpy as np

#Step 1: Initiate Population
population = 10000
population_list = agent.populate_Austin(population)

#Step 2: Initiate Neighbourhoods + Step 3: Define Commute Parameters
neighbourhood_list = neighbourhood.initiate_neighbourhoods(population_list)

#Step 3b: Update Initial Satisfaction of each Resident based on Initial Neighbourhood Characteristics

for resident in population_list:
    resident.update_satisfaction(neighbourhood_list)

#Step 4: Agent-Agent Monthly Interaction

months = 100

counts = [[],[],[]] #[west campus, north campus, riverside]

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


def plot_ridership():   
    X = np.arange(0, months, 1)
    #0/1/2 = west/north/riverside
    location = 0 

    # print(counts[location])
    walk = [list[3] for list in counts[location]]
    bus = [list[1] for list in counts[location]]
    bike = [list[2] for list in counts[location]]
    car = [list[0] for list in counts[location]]

    plt.figure("West Campus")
    plt.plot(X, walk, label = "walk")
    plt.plot(X, bus, label = "bus")
    plt.plot(X, bike, label = "bike")
    plt.plot(X, car, label = "car")
    plt.legend()


    location = 1 
    walk = [list[3] for list in counts[location]]
    bus = [list[1] for list in counts[location]]
    bike = [list[2] for list in counts[location]]
    car = [list[0] for list in counts[location]]

    plt.figure("North Campus")
    plt.plot(X, walk, label = "walk")
    plt.plot(X, bus, label = "bus")
    plt.plot(X, bike, label = "bike")
    plt.plot(X, car, label = "car")
    plt.legend()

    location = 2 
    walk = [list[3] for list in counts[location]]
    bus = [list[1] for list in counts[location]]
    bike = [list[2] for list in counts[location]]
    car = [list[0] for list in counts[location]]

    plt.figure("Riverside")
    plt.plot(X, walk, label = "walk")
    plt.plot(X, bus, label = "bus")
    plt.plot(X, bike, label = "bike")
    plt.plot(X, car, label = "car")
    plt.legend()

    plt.show()

plot_ridership()

