# Define neighbourhoods
# scores out of 10: drive, bus, bike, walk; convenience, speed, affordability, sustainability

import agent
import neighbourhood
import agent_env_periodically as aem
import agent_env_annual as aea


#Packages Needed
import matplotlib.pyplot as plt
import numpy as np
import test as unit
import plots as plot

#Plot Functions
neighbourhood_transit_history = [[] for i in range(3)] #[west campus, north campus, riverside], records ridership for [car, bus, bike, walk] each month
neighbourhood_score_history = [[] for i in range(3)] #[west campus, north campus, riverside], records scores for [car, bus, bike, walk] each month

#------------------------------------------------------------------------------------------------------------------------------------------------

#Tunable Model Inputs
population = 5000 #How big is the total student population?
years = 5 #How many years do we run the model?
periods_per_year = 52

#Agent Model Inputs
rent_percent_priority = 0.8 #How much % does rent cost affect overall affordability (rent + commute costs)?
satisfaction_bump_to_move = 0.2 #How much % increase in satisfaction does a student need to move neighbourhoods? 

student_types = ["Sustainability Oriented", "Convenience/Cost Oriented", "Cost Critical"] #What are the classification of student types?
student_types_percent = [0.1, 0.6, 0.3] #What percentage of total population is each student type?

sustainability_priorities = [0.2,0.2,0.2,0.4] #What percentages of [speed, convenience, affordability, sustainability] does this student value?
convenience_cost_priorities = [0.2,0.3,0.4,0.1] #[speed, convenience, affordability, sustainability] 
cost_critical_priorities = [0.1,0.1,0.7,0.1] #[speed, convenience, affordability, sustainability]

#Monthly Interaction Inputs

#priorities reflect interest in investing in the convenience, speed, affordability, and sustainability of car, bus, bike, pedestrian infrastructure; should sum to 4
city_priorities = [[0.1, 0.1, 0, 0],[0.3, 0.5, 0.2, 0.1],[0.3, 0.3, 0.1, 0],[0.3, 0.3, 0, 0]]  
city_priorities = city_priorities / np.sum(city_priorities)

#Fixed Model Inputs
months_per_year = periods_per_year
student_priority_profiles = [sustainability_priorities, convenience_cost_priorities, cost_critical_priorities]
transit_weights_monthly_update = []

#---------------------------------------------------------------------------------------------------------------------------

#Model

#Step 1: Initiate Population
population_list = agent.populate_Austin(population, rent_percent_priority, satisfaction_bump_to_move, student_types_percent, student_priority_profiles)
plot.record_neighbourhood_transit_history(population_list, neighbourhood_transit_history)

#Step 2: Initiate Neighbourhoods + Step 3: Define Commute Parameters
neighbourhood_list = neighbourhood.initiate_neighbourhoods(population_list)
plot.record_neighbourhood_score_history(neighbourhood_list, neighbourhood_score_history)

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

        plot.record_neighbourhood_score_history(neighbourhood_list, neighbourhood_score_history)

        #III: Residents Re-evaluate Satisfaction Relative to Last Month's Commutes and Chooses to Stay or Revert Back to Previous Commute
        for resident in population_list:
            resident.update_satisfaction(neighbourhood_list)
            resident.evaluate_commute_switch()

        #IV: Update transit history
        plot.record_neighbourhood_transit_history(population_list, neighbourhood_transit_history)
  

    #2. Annual Changes

    # # I. City Investments

    for neighbourhood in neighbourhood_list:
        aea.investment_update(neighbourhood, population, city_priorities)

    # # II. Rent Prices Systems Dynamics Update

    for neighbourhood in neighbourhood_list:
        neighbourhood.supply_demand()

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

plot.plot_ridership(months_per_year, years, neighbourhood_transit_history)
#plot.plot_score_history("West", "Driving", months_per_year, years, neighbourhood_score_history)
#plot.plot_all_score_histories(months_per_year, years, neighbourhood_score_history)
