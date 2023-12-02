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