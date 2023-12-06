import matplotlib.pyplot as plt
import numpy as np

def satisfaction_bar(population_list,student_types_percent):

    cumulative_types = np.cumsum(student_types_percent) * len(population_list)
    cumulative_types = np.insert(cumulative_types, 0, 0)

    satisfaction_by_type = []

    for i in range(3):
        students = population_list[int(cumulative_types[i]):int(cumulative_types[i + 1])]
        satisfactions = [student.satisfaction for student in students]
        satisfaction_by_type.append(satisfactions)

    plt.figure(figsize = (10,8))
    plt.boxplot(satisfaction_by_type, labels=['Sustainable', 'Cost / Convenience', 'Cost Critical'])
    plt.show()

def utilization_bar(population_list):
    
    utilizations = [student.transit for student in population_list]

    plt.figure(figsize = (10,8))
    plt.bar(utilizations, labels = ['Car','Bus','Bike','Walk'])
    plt.show()  

def transit_count(population_list):
    initial_transit = [0,0,0,0]
    for agent in population_list:
        initial_transit[agent.transit] += 1
    #print(initial_transit)
    return initial_transit

def record_neighbourhood_transit_history(population_list, neighbourhood_transit_history):
    def transit_neighbourhood_count():
        transit_count = [[0 for i in range(4)] for i in range(3)]
        for agent in population_list:
            transit_count[agent.neighbourhood][agent.transit] += 1
        #print(transit_count)
        return transit_count
    latest_count = transit_neighbourhood_count()
    for i in range(len(latest_count)):
        neighbourhood_transit_history[i].append(latest_count[i])

def record_neighbourhood_score_history(neighbourhood_list, neighbourhood_score_history):
    for neighbourhood in neighbourhood_list:
        scores =  neighbourhood.commutescores.copy()
        neighbourhood_score_history[neighbourhood.neighbourhood_id].append(scores)

def plot_ridership(months_per_year, years, neighbourhood_transit_history): 
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

def plot_score_history(neighbourhood, commute, months_per_year, years, neighbourhood_score_history): #("West/North/Riverside", "Driving/Bussing/Biking/Walking")
    X = np.arange(0, months_per_year*years + 1)

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

def plot_all_score_histories(months_per_year, years, neighbourhood_score_history):

    def plot_specific_score_history(neighbourhood, commute): #("West/North/Riverside", "Driving/Bussing/Biking/Walking")
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

    for neighbourhood in range(3):
        for commute in range(4):
            plot_specific_score_history(neighbourhood, commute)


def record_annual_rent(annual_rent_history, neighbourhood_list):
    reasonable_rent = 1200 #8/10
    reasonable_score = 8
    rent_price_delta_per_point = 200

    current_rent = [neighbourhood_list[0].rent, neighbourhood_list[1].rent, neighbourhood_list[2].rent]
    for i in range(len(current_rent)):
        score = current_rent[i]
        current_rent[i] = ((reasonable_score - score)*rent_price_delta_per_point + reasonable_rent)

    annual_rent_history.append(current_rent)

def plot_annual_rent(annual_rent_history, years):
    X = np.arange(1, years + 1)
    rent_history = annual_rent_history.copy()

    #0 = West, 1 = north, 2 = riverside
    west = []
    north = []
    riverside = []

    for year in range(years):
        west.append(rent_history[year][0])
        north.append(rent_history[year][1])
        riverside.append(rent_history[year][2])
    
    print(west)
    print(north)
    print(riverside)

    plt.figure("Rent Affordability")
    plt.plot(X, west, label = "West")
    plt.plot(X, north, label = "North")
    plt.plot(X, riverside, label = "Riverside")

    plt.legend()
    plt.show()


def record_student_type_neighbourhood_counts(population_list, student_types_percent, population):

    neighbourhood_counts = [[0,0,0] for i in range(3)] #[sustainability, cost/convenience, cost critical][west, north, riverside]
    population_per_archetype = [round(student_types_percent[i] * population) for i in range(3)]
    
    ranges = [population_per_archetype[0], population_per_archetype[0]+ population_per_archetype[1], population_per_archetype[0]+ population_per_archetype[1] + population_per_archetype[2]]
    
    neighbourhood_transit_counts = [[[0 for i in range(4)] for i in range (3)] for i in range(3)] #[sustainability, cost/convenience, cost critical][west, north, riverside][car, bus, bike, walk]
    #print(neighbourhood_transit_counts)


    for i in range(ranges[0]): #sustainability focused people
        student = population_list[i]
        neighbourhood_counts[0][student.neighbourhood] += 1
        neighbourhood_transit_counts[0][student.neighbourhood][student.transit] += 1

    for i in range(ranges[0], ranges[1]): #sustainability focused people
        student = population_list[i]
        neighbourhood_counts[1][student.neighbourhood] += 1
        neighbourhood_transit_counts[1][student.neighbourhood][student.transit] += 1

    for i in range(ranges[1], ranges[2]):
        neighbourhood_counts[2][student.neighbourhood] += 1
        neighbourhood_transit_counts[2][student.neighbourhood][student.transit] += 1
    
    # for neighbourhood in neighbourhood_counts:
    #     print(neighbourhood)

    print(neighbourhood_counts)
    print(neighbourhood_transit_counts)

    return [neighbourhood_counts,neighbourhood_transit_counts]

def plot_student_type_neighbourhood_counts(student_type_data, student_type):
    neighbourhood_counts = student_type_data[0]
    neighbourhood_transit_counts = student_type_data[1]

    plt.figure(figsize = (10,8))
    #plt.bar(['West', 'North', 'Riverside'], neighbourhood_counts[0], label = 'Sustainable Student')
    #plt.bar(['West', 'North', 'Riverside'], neighbourhood_counts[1], label = 'Cost/Convenience Student')
    plt.bar(['West', 'North', 'Riverside'], neighbourhood_counts[2], label = 'Cost Critical Student')
    plt.show()

    
    
    




