import numpy as np

# priorities reflect how much the government wants to invest in each commute type; four values total, should sum to 1

def investment_update(neighbourhood, population, priorities):

    annual_deltas = [0, 0, 0, 0]

    for i in range(4):

        # measure relative use
        annual_deltas[i] = (neighbourhood.annual_utilization[i] / population) * 12 - 1/12

        # make investments to baseline scores
        neighbourhood.baseline_scores[i] = calc_investment(neighbourhood.baseline_scores[i], annual_deltas[i], priorities[i])

        # return annual utilization to 0 for future accounting
        neighbourhood.annual_utilization[i] = 0

    # print(annual_deltas)
    
def calc_investment(baseline, delta, priority):

    if delta > 0:
        investment = delta * priority / 50
    else: 
        # if delta < 0, we see some divestment & deterioration
        investment = delta * (1 - priority) / 500
    
    #print(baseline)
    #print(delta)
    #print(investment)

    # convenience, speed, affordability, sustainability
    
    new_score = baseline + np.ones(4) * investment
    clip_score = np.clip(new_score, 0, 10)
    
    return clip_score