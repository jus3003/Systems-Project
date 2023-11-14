#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

class Agent:
    def __init__(self, id, neighbourhood, transit, priorities):
        #Variables that Initiates Change
        self.id = id
        self.neighbourhood = neighbourhood
        self.transit = transit
        self.satisfaction = 0 #no satisfaction when first moved in
        #Fixed Variables
        self.priorities = priorities #weighted list out of 1 [sustainability, speed, convenience, affordability]
        #Past/Future Variables
        self.transit_prev, self.transit_next, self.satisfaction_prev, self.satisfaction_next = 0, 0, 0, 0
        self.commutes_tried_in_curr_neighbourhood = []


# In[2]:


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

#test = priority_randomizer()


# In[7]:


#Create Population of Agents
def populate_Austin(population):
    population_list = []
    for i in range(0,population):
        assign_neighbourhood = random.randint(1,3) 
        assign_transit = random.randint(1,4) #1/2/3/4 = drive/bus/bike/walk
        assign_priorities = priority_randomizer()
        population_list.append(Agent(id = i, neighbourhood = assign_neighbourhood, transit = assign_transit, priorities = assign_priorities))
        #print(assign_neighbourhood, assign_priorities, assign_transit)

    return population_list

population = populate_Austin(20)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




