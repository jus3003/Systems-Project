import numpy as np

# priorities reflect how much the government wants to invest in each commute type; four values total, should sum to 1

def investment_update(neighbourhood, population, all_priorities):

    annual_deltas = [0, 0, 0, 0]

    for i in range(4):

        # measure relative use
        # Why * 12?
        annual_deltas[i] = (neighbourhood.annual_utilization[i] / population) * 12 - 1/12

        # make investments to baseline scores
        neighbourhood.baseline_scores[i] = calc_investment(neighbourhood.baseline_scores[i], annual_deltas[i], all_priorities[i])

        # return annual utilization to 0 for future accounting
        neighbourhood.annual_utilization[i] = 0
    
def calc_investment(baseline, delta, priorities):

    #priorities reflect interest in investing in the convenience, speed, affordability, and sustainability of car, bus, bike, pedestrian infrastructure; should sum to 4
    #city_priorities = [[0.3, 0.3, 0.2, 0.2],[0.2, 0.5, 0.2, 0.1],[0.5, 0.4, 0.1, 0],[0.7, 0.3, 0, 0]]  

    if delta > 0:
        investment = delta * np.array(priorities) / 50
    else: 
        # if delta < 0, we see some divestment & deterioration
        investment = delta * (np.ones(4) - np.array(priorities)) / 500
    
    #print(baseline)
    #print(delta)
    #print(investment)

    # convenience, speed, affordability, sustainability
    
    new_score = baseline + investment
    clip_score = np.clip(new_score, 0, 10)
    
    return clip_score