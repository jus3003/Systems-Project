#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Neighbourhood:

    def __init__(self, rent, commutescores, neighbourhood_id):

        self.rent = rent
        self.neighbourhood_id = neighbourhood_id

        # commute scores will be a nested list
        # lists are for drive; bus; bike; walk
        # list elements are convenience; speed; affordability; sustainability

        self.commutescores = commutescores

        # this will later be used for identifying commute utilization

        self.resident_list = []

        self.annual_utilization = [0, 0, 0, 0]

        self.transit_counts = [0,0,0,0]

    # get_residents occurs yearly to update populations
    # pass in total population of Austin

    def define_residents(self, population):

        self.resident_list = []

        for agent in population:
            if agent.neighbourhood == self.neighbourhood_id:
                self.resident_list.append(agent)

    def count_transit(self):

        self.transit_counts = [0,0,0,0] #resets list 

        for resident in self.resident_list:
            self.transit_counts[resident.transit] += 1


    # convenience and speed update on a yearly basis due to investment; this will actually go in a separate tab
    # city_priorities is an array for interest in investing in infrastructure for [cars, busses, bikes, pedestrians]

    def yearly_investment(self, city_priorities):

        for i in range(4):
            self.commutescores[i][0] = self.commutescores[i][0] + self.annual_utilization[i] * city_priorities[i] / 100
            self.commutescores[i][1] = self.commutescores[i][1] + self.annual_utilization[i] * city_priorities[i] / 100


# In[2]:


# Define neighbourhoods (this may go in main)
# scores out of 10: drive, bus, bike, walk; convenience, speed, affordability, sustainability

# using population = populate_Austin(n)

def initiate_neighbourhoods(population):

    # commute scores will be a nested list
    # lists are for drive; bus; bike; walk
    # list elements are convenience; speed; affordability; sustainability

    west_scores = [[8, 9, 2, 3], [5, 5, 10, 8], [7, 9, 7, 9], [8, 6, 10, 10]]
    north_scores = [[9, 9, 2, 3], [7, 8, 10, 8], [9, 9, 8, 9], [8, 5, 10, 10]]
    riverside_scores = [[8, 7, 2, 2], [7, 3, 10, 7], [4, 3, 8, 9], [1, 1, 10, 10]]

    west = Neighbourhood(6,west_scores, 0)

    north = Neighbourhood(7,north_scores, 1)

    riverside = Neighbourhood(9,riverside_scores, 2)

    all_neighbourhoods = [west, north, riverside]

    for neighbourhood in all_neighbourhoods:
        neighbourhood.define_residents(population)
        neighbourhood.housing_supply = len(neighbourhood.resident_list)
        neighbourhood.count_transit()
        neighbourhood.baseline_scores = neighbourhood.commutescores
        neighbourhood.score_history = []


    return all_neighbourhoods



# In[3]:




