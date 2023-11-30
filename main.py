# Define neighbourhoods
# scores out of 10: drive, bus, bike, walk; convenience, speed, affordability, sustainability

import agent
import neighbourhoodclass as neighbourhood 
import agent_env_monthly as aem
import agent_env_annual as aea
import test as unit

#Packages Needed
import matplotlib.pyplot as plt
import numpy as np

#Functions
def transit_count():
    initial_transit = [0,0,0,0]
    for agent in population_list:
        initial_transit[agent.transit] += 1
    #print(initial_transit)
    return initial_transit

def record_neighbourhood_transit_history():
    def transit_neighbourhood_count():
        transit_count = [[0 for i in range(4)] for i in range(3)]
        for agent in population_list:
            transit_count[agent.neighbourhood][agent.transit] += 1
        #print(transit_count)
        return transit_count
    latest_count = transit_neighbourhood_count()
    for i in range(len(latest_count)):
        neighbourhood_transit_history[i].append(latest_count[i])

def record_neighbourhood_score_history():
    for neighbourhood in neighbourhood_list:
        scores =  neighbourhood.commutescores.copy()
        neighbourhood_score_history[neighbourhood.neighbourhood_id].append(scores)

#Plot Functions
def plot_ridership(): 
    X = np.arange(0, months_per_year*years + 1)

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

def plot_score_history(neighbourhood, commute): #("West/North/Riverside", "Driving/Bussing/Biking/Walking")
    X = np.arange(0, months_per_year*years + 1)

    # neighbourhood_name = {0: "West Campus", 1: "North Campus", 2: "Riverside"}
    # commute_name = {0: "Driving", 1: "Bussing", 2: "Biking", 3: "Walking"}

    # neighbourhood_history = neighbourhood_score_history[neighbourhood]

    # convenience = [list[commute][0]for list in neighbourhood_history]
    # speed = [list[commute][1]for list in neighbourhood_history]
    # affordability = [list[commute][2]for list in neighbourhood_history]
    # sustainability = [list[commute][3]for list in neighbourhood_history]

    # plt.figure(f"{commute_name[commute]} from {neighbourhood_name[neighbourhood]}")
    
    # plt.plot(X, convenience, label = "convenience")
    # plt.plot(X, speed, label = "speed")
    # plt.plot(X, affordability, label = "affordability")
    # plt.plot(X, sustainability, label = "sustainability")
    # plt.legend()
    # plt.show()

    neighbourhood_index = {"West": 0, "North": 1, "Riverside":2}
    commute_name = {"Driving": 0, "Bussing": 1, "Biking" : 2, "Walking": 3}

    neighbourhood_history = neighbourhood_score_history[neighbourhood_index[neighbourhood]] 

    convenience = [list[commute_name[commute]][0]for list in neighbourhood_history]
    speed = [list[commute_name[commute]][1]for list in neighbourhood_history]
    affordability = [list[commute_name[commute]][2]for list in neighbourhood_history]
    sustainability = [list[commute_name[commute]][3]for list in neighbourhood_history]

    plt.figure(f"Scores for {commute} from {neighbourhood}")
    plt.plot(X, convenience, label = "convenience")
    plt.plot(X, speed, label = "speed")
    plt.plot(X, affordability, label = "affordability")
    plt.plot(X, sustainability, label = "sustainability")
    plt.legend()
    plt.show()

def plot_all_score_histories():

    def plot_score_history(neighbourhood, commute): #("West/North/Riverside", "Driving/Bussing/Biking/Walking")
        X = np.arange(0, months_per_year*years + 1)

        neighbourhood_name = {0: "West Campus", 1: "North Campus", 2: "Riverside"}
        commute_name = {0: "Driving", 1: "Bussing", 2: "Biking", 3: "Walking"}

        neighbourhood_history = neighbourhood_score_history[neighbourhood]

        convenience = [list[commute][0]for list in neighbourhood_history]
        speed = [list[commute][1]for list in neighbourhood_history]
        affordability = [list[commute][2]for list in neighbourhood_history]
        sustainability = [list[commute][3]for list in neighbourhood_history]

        plt.figure(f"{commute_name[commute]} from {neighbourhood_name[neighbourhood]}")
        
        plt.plot(X, convenience, label = "convenience")
        plt.plot(X, speed, label = "speed")
        plt.plot(X, affordability, label = "affordability")
        plt.plot(X, sustainability, label = "sustainability")
        plt.legend()
        plt.show()

    for i in range(3):
        for j in range(4):
            plot_score_history(i,j)

#Tunable Model Inputs
population = 10000 #How big is the total student population?
years = 5 #How many years do we run the model?

#Agent Model Inputs
rent_percent_priority = 0.8 #How much % does rent cost affect overall affordability?
satisfaction_bump_to_move = 0.2 #How much % increase in satisfaction does a student need to move neighbourhoods? 

student_types = ["Sustainability Oriented", "Convenience/Cost Oriented", "Cost Critical"] #What are the classification of student types?
student_types_percent = [0.1, 0.6, 0.3] #What percentage of total population is each student type?

sustainability_priorities = [0.2,0.2,0.2,0.4] #What percentages of [speed, convenience, affordability, sustainability] does this student value?
convenience_cost_priorities = [0.2,0.3,0.4,0.1] #[speed, convenience, affordability, sustainability] 
cost_critical_priorities = [0.1,0.1,0.7,0.1] #[speed, convenience, affordability, sustainability]

#Other
city_priorities = [0.2, 0.5, 0.2, 0.1]  #priorities reflect interest in car, bus, bike, pedestrian infrastructure; should sum to 4


#Fixed Model Inputs
months_per_year = 12
student_priority_profiles = [sustainability_priorities, convenience_cost_priorities, cost_critical_priorities]

#----------------------------------------------------------------------------------

#Model

#Step 1: Initiate Population
population_list = agent.populate_Austin(population, rent_percent_priority, satisfaction_bump_to_move, student_types_percent, student_priority_profiles)
neighbourhood_transit_history = [[] for i in range(3)] #[west campus, north campus, riverside], records ridership for [car, bus, bike, walk] each month
neighbourhood_score_history = [[] for i in range(3)] #[west campus, north campus, riverside], records scores for [car, bus, bike, walk] each month
record_neighbourhood_transit_history()

#Step 2: Initiate Neighbourhoods + Step 3: Define Commute Parameters
neighbourhood_list = neighbourhood.initiate_neighbourhoods(population_list)
record_neighbourhood_score_history()

#Step 3: Update Initial Satisfaction of each Resident based on Initial Neighbourhood Characteristics
for resident in population_list:
    resident.update_satisfaction(neighbourhood_list)

#Step 4: Start Model Run for # of Years
for year in range(years):

    #1. Monthly Changes
    for month in range(months_per_year):

        #I: Compare with Random Neighbour + Switch Transit if Satisfaction is Greater
        for resident in population_list:
            resident.monthly_neighbour_interaction(neighbourhood_list)

        #II: Monthly Agent-Environment Interaction (evaluates system performance after transit changes and updates self.commute_scores descriptors for each neighbourhood)
        for neighbourhood in neighbourhood_list:
            aem.commute_update(neighbourhood,population)

        record_neighbourhood_score_history()

        #III: Residents Re-evaluate Satisfaction Relative to Last Month's Commutes and Chooses to Stay or Revert Back to Previous Commute
        for resident in population_list:
            resident.update_satisfaction(neighbourhood_list)
            resident.evaluate_commute_switch()

        #IV: Update transit history
        record_neighbourhood_transit_history()
  

    #2. Annual Changes

    # # I. City Investments

    # for neighbourhood in neighbourhood_list:
    #     aea.investment_update(neighbourhood, population, city_priorities)

    # # II. Rent Prices Systems Dynamics Update

    # for neighbourhood in neighbourhood_list:
    #     neighbourhood.supply_demand()

    # III. Residents Update Satisfaction based on City Investments and New Rent Prices

    for resident in population_list:
        resident.update_satisfaction(neighbourhood_list)
    
    # IV. Annual Agent-Agent Interaction, Consider Moving Neighourhoods

    for resident in population_list:
        resident.annual_neighbour_interaction(population_list)
        resident.update_satisfaction(neighbourhood_list)

    # V. Update neighbourhood resident lists for the new year

    for neighbourhood in neighbourhood_list:
        neighbourhood.define_residents(population_list)

    #unit.test_1(neighbourhood_list)


#Plot Checks

plot_ridership()
#plot_score_history("West", "Driving")
#plot_all_score_histories()
