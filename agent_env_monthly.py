import numpy as np

def commute_update(neighbourhood, population):
    
    neighbourhood.monthly_utilization = [0, 0, 0, 0]
    
    # convenience updates on a monthly basis due to congestion
    for agent in neighbourhood.resident_list:
        
        neighbourhood.monthly_utilization[agent.transit] += 1
        
    # track utilization to inform annual investments
    neighbourhood.annual_utilization += neighbourhood.monthly_utilization

    # congestion effects

    # cars: all scores effected
    car_delta = neighbourhood.monthly_utilization[0] / population - 1/12
    car_baseline = neighbourhood.baseline_scores[0]
    car_weights = [0.25, 0.25, 0.2, 0.2]

    neighbourhood.commutescores[0] = calculate_score(car_delta, car_baseline, car_weights)

    # bus: mild impacts on convenience and speed
    bus_delta = neighbourhood.monthly_utilization[1] / population - 1/12
    bus_baseline = neighbourhood.baseline_scores[1]
    bus_weights = [0.15, 0.15, 0, 0]

    neighbourhood.commutescores[1] = calculate_score(bus_delta, bus_baseline, bus_weights) 

    # bike: very mild impacts on convenience
    bike_delta = neighbourhood.monthly_utilization[2] / population - 1/12
    bike_baseline =neighbourhood.baseline_scores[2]
    bike_weights = [0.1, 0, 0, 0]
    neighbourhood.commutescores[2] = calculate_score(bike_delta, bike_baseline, bike_weights)

    # walk: very mild impacts on convenience
    walk_delta = neighbourhood.monthly_utilization[3] / population - 1/12
    walk_baseline = neighbourhood.baseline_scores[3]
    walk_weights = [0.05, 0, 0, 0]
    neighbourhood.commutescores[3] = calculate_score(walk_delta, walk_baseline, walk_weights)

def calculate_score(deltas, baseline, weights):

    weights = np.array(weights)
    baseline = np.array(baseline)
    deltas = np.array(deltas)

    # calculate the score for each element
    scores = baseline + weights * deltas

    # clip the scores
    scores = np.clip(scores, 0, 10)
    print(scores)

    return scores