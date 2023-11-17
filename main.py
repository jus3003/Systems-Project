# Define neighbourhoods
# scores out of 10: drive, bus, bike, walk; convenience, speed, affordability, sustainability

import agent
import neighbourhoodclass as neighbourhood 
import agent_env_monthly as aem
import matplotlib.pyplot as plt
import numpy as np

#Model Inputs
population = 10000
months = 60

#Step 1: Initiate Population
population_list = agent.populate_Austin(population)
neighbourhood_transit_history = [[] for i in range(3)] #[west campus, north campus, riverside]

def transit_count():
    initial_transit = [0,0,0,0]
    for agent in population_list:
        initial_transit[agent.transit] += 1
    #print(initial_transit)
    return initial_transit
def transit_neighbourhood_count():
    transit_count = [[0 for i in range(4)] for i in range(3)]
    for agent in population_list:
        transit_count[agent.neighbourhood][agent.transit] += 1
    #print(transit_count)
    return transit_count
def update_history():
    latest_count = transit_neighbourhood_count()
    for i in range(len(latest_count)):
        neighbourhood_transit_history[i].append(latest_count[i])

update_history()

#Step 2: Initiate Neighbourhoods + Step 3: Define Commute Parameters
neighbourhood_list = neighbourhood.initiate_neighbourhoods(population_list)

#Step 3b: Update Initial Satisfaction of each Resident based on Initial Neighbourhood Characteristics

for resident in population_list:
    resident.update_satisfaction(neighbourhood_list)

#Step 4: Agent-Agent Monthly Interaction

for i in range(months):

    #4a: Compare with Random Neighbour + Switch Transit if Satisfaction is Greater
    for resident in population_list:
        resident.monthly_neighbour_interaction(neighbourhood_list)

    #5: Monthly Agent-Environment Interaction (evaluates system performance after transit changes and updates self.commutescores descriptors for each neighbourhood)
    for neighbourhood in neighbourhood_list:
        neighbourhood.commute_scores = aem.commute_update(neighbourhood,population)

    #4b: Residents Re-evaluate Satisfaction Relative to Last Month's Commutes and Chooses to Stay or Revert Back to Previous Commute
    for resident in population_list:
        resident.update_satisfaction(neighbourhood_list)
        resident.evaluate_commute_switch()

    #4c: Update transit history
    update_history()      

def plot_ridership():   
    X = np.arange(0, months + 1)

    #0/1/2 = west/north/riverside
    location = 0 

    # print(counts[location])
    walk = [list[3] for list in neighbourhood_transit_history[location]]
    bus = [list[1] for list in neighbourhood_transit_history[location]]
    bike = [list[2] for list in neighbourhood_transit_history[location]]
    car = [list[0] for list in neighbourhood_transit_history[location]]

    plt.figure("West Campus")
    plt.plot(X, walk, label = "walk")
    plt.plot(X, bus, label = "bus")
    plt.plot(X, bike, label = "bike")
    plt.plot(X, car, label = "car")
    plt.legend()

    location_1 = 1 
    walk_1 = [list[3] for list in neighbourhood_transit_history[location_1]]
    bus_1 = [list[1] for list in neighbourhood_transit_history[location_1]]
    bike_1 = [list[2] for list in neighbourhood_transit_history[location_1]]
    car_1 = [list[0] for list in neighbourhood_transit_history[location_1]]

    plt.figure("North Campus")
    plt.plot(X, walk_1, label = "walk")
    plt.plot(X, bus_1, label = "bus")
    plt.plot(X, bike_1, label = "bike")
    plt.plot(X, car_1, label = "car")
    plt.legend()

    location_2 = 2 
    walk_2 = [list[3] for list in neighbourhood_transit_history[location_2]]
    bus_2 = [list[1] for list in neighbourhood_transit_history[location_2]]
    bike_2 = [list[2] for list in neighbourhood_transit_history[location_2]]
    car_2 = [list[0] for list in neighbourhood_transit_history[location_2]]

    plt.figure("Riverside")
    plt.plot(X, walk_2, label = "walk")
    plt.plot(X, bus_2, label = "bus")
    plt.plot(X, bike_2, label = "bike")
    plt.plot(X, car_2, label = "car")
    plt.legend()

    plt.show()

plot_ridership()