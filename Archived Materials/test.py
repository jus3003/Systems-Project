def test_0(population_list, neighbourhood_list): #tests rent price updating affordability metric #test passed
    test = population_list[1]
    neigh = neighbourhood_list[test.neighbourhood]
    print(f"agent {test.id} has {test.priorities} priorities")
    print(f"agent lives in neighbourhood {test.neighbourhood} and {test.transit}")
    print(f"their neighbourhood has commute scores of {neigh.commutescores} and rent score of {neigh.rent} ")
    print(f"their satisfaction is {test.satisfaction}")

def test_1(neighbourhood_list): #tests neighbourhood residents
    print(f"Neighbourhood 0 has {len(neighbourhood_list[0].resident_list)} residents")
    print(f"Neighbourhood 1 has {len(neighbourhood_list[1].resident_list)} residents")
    print(f"Neighbourhood 2 has {len(neighbourhood_list[2].resident_list)} residents")
    print("--------- Year End --------------------")