# Define neighbourhoods
# scores out of 10: drive, bus, bike, walk; convenience, speed, affordability, sustainability

import agent
import neighbourhoodclass as neighbourhood 


#Step 1: Initiate Population
population = 10
population_list = agent.populate_Austin(population)

#Step 2: Initiate Neighbourhoods + Step 3: Define Commute Parameters
neighbourhood_list = neighbourhood.initiate_neighbourhoods(population_list)

#Step 3b: Update Initial Satisfaction of each Resident based on Initial Neighbourhood Characteristics

for resident in population_list:
    resident.update_satisfaction(neighbourhood_list)

#Step 4: Agent-Agent Monthly Interaction

for neighbourhood in neighbourhood_list:
    print(f"neighbourhood #: {neighbourhood.neighbourhood_id}")
    for resident in neighbourhood.resident_list:
        print(f"resident # {resident.id}")

test = population_list[0]
print(test.id)
test.monthly_agent_interaction(neighbourhood_list)






