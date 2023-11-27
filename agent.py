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
        self.transit_prev, self.transit_next, self.satisfaction_prev, self.satisfaction_next = -1, -1, -1, -1
        self.testing_commute_option = False
        self.commutes_tried_in_curr_neighbourhood = []
        self.neighbourhood_change_threshold = 0.2
        self.neighbourhood_prev_annual, self.neighbourhood_satisfaction_prev_annual, self.transit_prev_annual = 0, 0, 0

    def update_transit(self, transit_type):
        self.transit = transit_type

    def update_satisfaction(self, neighbourhood_list): #metrics_list = [convenience, speed, affordability, sustainability] -> scored /10 for each category
        neighbourhood = neighbourhood_list[self.neighbourhood]
        metrics_list = neighbourhood.commutescores[self.transit] #grabs commute scores for current neighbourhood and mode of transit
        metrics_list[2] = 0.2*metrics_list[2] + 0.8*neighbourhood.rent #factor rental costs into affordability score
        self.satisfaction = sum([a*b for a,b in zip(metrics_list, self.priorities)]) #calculates satisfaction

    def monthly_neighbour_interaction(self, neighbourhood_list):
        neighbours = neighbourhood_list[self.neighbourhood].resident_list

        interacting_agent = neighbours[random.randint(0,len(neighbours)-1)]
        while (interacting_agent.id == self.id): #Checks that we don't select ourselves to talk to 
            interacting_agent = neighbours[random.randint(0,len(neighbours)-1)]

        #Save current transit and satisfaction history prior to trying new transit option
        self.transit_prev, self.satisfaction_prev = self.transit, self.satisfaction

        #Only switch transit options if satisfactions is greater
        if (interacting_agent.satisfaction > self.satisfaction):
            self.transit = interacting_agent.transit
            self.satisfaction = -1 #Set to -1 to indicate it needs to be re-evaluated since new commute is tried

    def evaluate_commute_switch(self):
        if (self.satisfaction_prev > self.satisfaction):
            self.transit, self.transit_prev = self.transit_prev, self.transit #swap back
        
    def annual_neighbour_interaction(self, population_list):
        interacting_agent = population_list[random.randint(0,len(population_list))]

        if (interacting_agent.neighbourhood == self.neighbourhood): #if same neighbourhood, no change
            return

        if (interacting_agent.satisfaction < (1+self.neighbourhood_change_threshold)*(self.satisfaction)): #if satisfaction less than required satisfaction bump to move neighbourhoods, no change
            return
        
        if (interacting_agent.satisfaction < self.neighbourhood_satisfaction_prev_annual): #if recommendation worse than previous years neighbourhood/transit combo, switch back to old combo
            #record current neighbourhood/transit/satisfaction as previous years
            #update current neighbourhood/transit/satisfaction to current years
            pass
        else: #change to neighbours recomendation
            pass


        # if (self.neighbourhood_satisfaction_prev > interacting_agent.satisfaction): #if satisfaction in previous neighbourhood is greater than neighbours satisfaction, go back to previous neighbourhood/transit setup
        #     self.neighbourhood = self.neighbourhood_prev
        #     self.transit, self.transit_prev = 
        # else:
        #     self.neihgbourhood, self.transit = 

        # self.neighbourhood_prev, self.neighbourhood_satisfaction_prev = self.neighbourhood, self.satisfaction
        

        
            
            

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


