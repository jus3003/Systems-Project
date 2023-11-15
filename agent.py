import random

class Agent:
    def __init__(self, id, neighbourhood, transit, priorities):
        #Variables that Initiates Change
        self.id = id
        self.neighbourhood = neighbourhood #0/1/2 = west/north/riverside
        self.transit = transit #0/1/2/3 = drive/bus/bike/walks
        self.satisfaction = 0  #no satisfaction when first moved in
        #Fixed Variables
        self.priorities = priorities #weighted list out of 1 [convenience, speed, affordability, sustainability]
        #Past/Future Variables
        self.transit_prev, self.transit_next, self.satisfaction_prev, self.satisfaction_next = 0, 0, 0, 0
        self.commutes_tried_in_curr_neighbourhood = []

    def update_transit(self, transit_type):
        self.transit = transit_type

    def update_satisfaction(self, neighbourhood_list): #metrics_list = [convenience, speed, affordability, sustainability] -> scored /10 for each category
        metrics_list = neighbourhood_list[self.neighbourhood].commutescores[self.transit] #grabs scores for current neighbourhood and mode of transit
        self.satisfaction = sum([a*b for a,b in zip(metrics_list, self.priorities)])

    def monthly_agent_interaction(self, neighbourhood_list):
        neighbours = neighbourhood_list[self.neighbourhood].resident_list

        interacting_agent = neighbours[random.randint(0,len(neighbours)-1)]
        while (interacting_agent.id == self.id): #Checks that we don't select ourselves to tak to 
            interacting_agent = neighbours[random.randint(0,len(neighbours)-1)]

        print(interacting_agent.id)

        

#Create Population of Agents
def populate_Austin(population):

    #Randomize Priorities of Agents
    def priority_randomizer():
        random_range = random.randint(1,10)
        priorities = []
        sum = 0
        
        for i in range(4):
            num = random.randint(1,random_range)
            priorities.append(num)
            sum += num
        for i in range(len(priorities)):
            priorities[i] /= sum

        #print("[sustainability, speed, convenience, affordability] = ", priorities)
        return priorities #[sustainability, speed, convenience, affordability]

    #Create Population List
    population_list = []
    for i in range(0,population):
        assign_neighbourhood = random.randint(0,2) 
        assign_transit = random.randint(0,3) #0/1/2/3 = drive/bus/bike/walk
        assign_priorities = priority_randomizer()
        population_list.append(Agent(id = i, neighbourhood = assign_neighbourhood, transit = assign_transit, priorities = assign_priorities))
        #print(assign_neighbourhood, assign_priorities, assign_transit)

    return population_list

#population_list = populate_Austin(20)


