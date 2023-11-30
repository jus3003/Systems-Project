import random

class Agent:
    def __init__(self, id, neighbourhood, transit, priorities, rent_percent_priority, satisfaction_bump_to_move):
        #Variables that Initiates Change
        self.id = id
        self.neighbourhood = neighbourhood #0/1/2 = west/north/riverside
        self.transit = transit #0/1/2/3 = drive/bus/bike/walks
        self.satisfaction = 0  #no satisfaction when first moved in     

        #Fixed Variables
        self.priorities = priorities #weighted list out of 1 [convenience, speed, affordability, sustainability]
        self.rent_percent_priority = rent_percent_priority # Percentage that rent prices affect affordability
        
        #Past/Future Variables
        self.transit_prev, self.transit_next, self.satisfaction_prev, self.satisfaction_next = -1, -1, -1, -1
        self.testing_commute_option = False
        self.commutes_tried_in_curr_neighbourhood = []
        self.neighbourhood_change_threshold = satisfaction_bump_to_move
        self.neighbourhood_prev_annual, self.neighbourhood_satisfaction_prev_annual, self.transit_prev_annual = None, self.satisfaction, None

    def update_transit(self, transit_type):
        self.transit = transit_type

    def update_satisfaction(self, neighbourhood_list): #metrics_list = [convenience, speed, affordability, sustainability] -> scored /10 for each category
        neighbourhood = neighbourhood_list[self.neighbourhood]
        metrics_list = neighbourhood.commutescores[self.transit].copy() #grabs commute scores for current neighbourhood and mode of transit
        metrics_list[2] = (1-self.rent_percent_priority)*metrics_list[2] + self.rent_percent_priority*neighbourhood.rent #factor rental costs into affordability score
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
        interacting_agent = population_list[random.randint(0,len(population_list)-1)]

        satisfaction_to_change = (1+self.neighbourhood_change_threshold)*(self.satisfaction) #min satisfaction bump to change neighbourhoods

        def test():
            if (self.id == 1): #testing code
                # print(f"Agent {self.id} lives in {self.neighbourhood} and uses {self.transit} and has satisfaction of {self.satisfaction:.3f}")
                # print(f"Agent interacts with Bob-{interacting_agent.id}")
                # print(f"Bob     lives in {interacting_agent.neighbourhood} and uses {interacting_agent.transit} and has satisfaction of {interacting_agent.satisfaction:.3f}")
                # print(f"To move to another neighbourhood, Agent needs a satisfaction of {satisfaction_to_change:.3f}")
                # print(f"Agents current satisfaction is {self.satisfaction:.3f}, past is {self.neighbourhood_satisfaction_prev_annual:.3f}, recommender has {interacting_agent.satisfaction:.3f}")
                
                #print("------------------------year end ----------------")
                print(f"satisfaction to change {satisfaction_to_change:.3f}")
                print()
                print("Past Agent ..........")
                print(f"neighbourhood {self.neighbourhood_prev_annual}, satisfaction {self.neighbourhood_satisfaction_prev_annual:.3f}, transit {self.transit_prev_annual}")
                print("Current Agent.......")
                print(f"neighbourhood {self.neighbourhood}, satisfaction {self.satisfaction:.3f}, transit {self.transit}")
                print("Friend..........")
                print(f"neighbourhood {interacting_agent.neighbourhood}, satisfaction {interacting_agent.satisfaction:.3f}, transit {interacting_agent.transit}")
                print()
                print("        comparison begins       ")
                print()  
        #test()
        
        #if no previous housing history, test out current housing history for one more year. 

        if (self.neighbourhood_prev_annual == None): 
            self.neighbourhood_prev_annual, self.neighbourhood_satisfaction_prev_annual, self.transit_prev_annual = self.neighbourhood, self.satisfaction, self.transit
            return
        
        #Otherwise, interact with neighbour and compare neighbour satisfaction with current satisfaction and last years satisfaction to determine which neighbourhood to live in

        if ((interacting_agent.satisfaction > self.neighbourhood_satisfaction_prev_annual) and (interacting_agent.satisfaction > satisfaction_to_change)): #if neighbour recommendation is strongest
            self.neighbourhood_prev_annual, self.neighbourhood_satisfaction_prev_annual, self.transit_prev_annual = self.neighbourhood, self.satisfaction, self.transit #record this year's neighbourhood and satisfaction as past for new year
            
            if(interacting_agent.neighbourhood == self.neighbourhood): #if same neighbourhood, no switch
                pass
            else: #take on neighbourhood/transit of recommended
                self.neighbourhood, self.transit = interacting_agent.neighbourhood, interacting_agent.transit
                      
        elif ((self.neighbourhood_satisfaction_prev_annual > interacting_agent.satisfaction) and (self.neighbourhood_satisfaction_prev_annual > satisfaction_to_change)): #if previous neighbourhood was strongest
            if(interacting_agent.neighbourhood == self.neighbourhood): #if same neighbourhood, no switch
                self.neighbourhood_prev_annual, self.neighbourhood_satisfaction_prev_annual, self.transit_prev_annual = self.neighbourhood, self.satisfaction, self.transit #record this year's neighbourhood and satisfaction as past for new year
            else:  #record current satisfaction as previous, swap back neighbourhoods and record current neighbourhood as previous, swap back transit and record current transit as previous
                self.neighbourhood_satisfaction_prev_annual = self.satisfaction
                self.neighbourhood, self.neighbourhood_prev_annual = self.neighbourhood_prev_annual, self.neighbourhood             
                self.transit, self.transit_prev_annual = self.transit_prev_annual, self.transit 

        else: #if current neighbourhood is strongest
            self.neighbourhood_prev_annual, self.neighbourhood_satisfaction_prev_annual, self.transit_prev_annual = self.neighbourhood, self.satisfaction, self.transit #record this year's neighbourhood stats as past for new year

        #need to update satisfaction in main.py for this specific agent everytime there is an annual-neighbour-interaction
        
        def test_b():
            if (self.id == 1):
                print(f"satisfaction to change {satisfaction_to_change:.3f}") 
                print()
                print("Past Agent ..........")
                print(f"neighbourhood {self.neighbourhood_prev_annual}, satisfaction {self.neighbourhood_satisfaction_prev_annual:.3f}, transit {self.transit_prev_annual}")
                print("Current Agent.......")
                print(f"neighbourhood {self.neighbourhood}, satisfaction {self.satisfaction:.3f}, transit {self.transit}")
                print("Friend..........")
                print(f"neighbourhood {interacting_agent.neighbourhood}, satisfaction {interacting_agent.satisfaction:.3f}, transit {interacting_agent.transit}")

                print()
                print("-------------------Year End -------------------")
                print()
        #test_b()

#Create Population of Agents



def populate_Austin(population, rent_percent_priority, satisfaction_bump_to_move): #Includes Agent Profiles

    #Randomize Priorities of Agents
    def priority_randomizer(approx_priorities):
        priorities = []
        sum = 0
        
        for i in range(4):
            # priorities are approximated as an input, but drawn from a distribution around +/- 20% of the approximation
            num = random.uniform(approx_priorities[i]*0.8,approx_priorities[i]*1.2)
            priorities.append(num)
            sum += num
        for i in range(len(priorities)):
            priorities[i] /= sum

        #print("[speed, convenience, affordability, sustainability] = ", priorities)
        return priorities #[speed, convenience, affordability, sustainability]

    # Create Population List
    population_list = []

    # Synthetic population: 10% sustainability oriented; 60% convenience/cost oriented; 30% cost critical
    sus_pop = int(0.1 * population)
    conv_pop = int(0.6 * population)
    cost_pop = population - sus_pop - conv_pop


    for i in range(0,sus_pop):
        assign_neighbourhood = random.randint(0,2) 
        assign_transit = random.randint(0,3) #0/1/2/3 = drive/bus/bike/walk)
        assign_priorities = priority_randomizer([0.2,0.2,0.2,0.4]) #20% speed, 20% convenience, 20% affordability, 40% sustainability
        population_list.append(Agent(id = i, neighbourhood = assign_neighbourhood, transit = assign_transit, priorities = assign_priorities, rent_percent_priority = rent_percent_priority, satisfaction_bump_to_move = satisfaction_bump_to_move))
        #print(assign_neighbourhood, assign_priorities, assign_transit)

    for i in range(0,conv_pop):
        assign_neighbourhood = random.randint(0,2) 
        assign_transit = random.randint(0,3) #0/1/2/3 = drive/bus/bike/walk)
        assign_priorities = priority_randomizer([0.2,0.3,0.4,0.1]) #20% speed, 30% convenience, 40% affordability, 10% sustainability
        population_list.append(Agent(id = i, neighbourhood = assign_neighbourhood, transit = assign_transit, priorities = assign_priorities, rent_percent_priority = rent_percent_priority, satisfaction_bump_to_move = satisfaction_bump_to_move))
        #print(assign_neighbourhood, assign_priorities, assign_transit)

    for i in range(0, cost_pop):
        assign_neighbourhood = random.randint(0,2) 
        assign_transit = random.randint(0,3) #0/1/2/3 = drive/bus/bike/walk)
        assign_priorities = priority_randomizer([0.1,0.1,0.7,0.1]) #10% speed, 10% convenience, 70% affordability, 10% sustainability
        population_list.append(Agent(id = i, neighbourhood = assign_neighbourhood, transit = assign_transit, priorities = assign_priorities, rent_percent_priority = rent_percent_priority, satisfaction_bump_to_move = satisfaction_bump_to_move))
        #print(assign_neighbourhood, assign_priorities, assign_transit)

    return population_list

#population_list = populate_Austin(20)


