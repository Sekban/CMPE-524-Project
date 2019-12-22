import csv
import math
import time
import numpy as np
from GreedyApproach import Greedy
from SimulatedAnnealing import SimulatedAnnealing

data_directory_keywords = ['No_of_Concentrators', 'Initial_Temp_SA', 'Final_Temp_SA', 'No_of_Terminals', 'No_of_Cycles_SA', 'No_of_Iterations_SA']
test_size_keywords = ['Test_Large', 'Test_Small']


if __name__ == "__main__":    
  for data_directory_keyword in data_directory_keywords:
    for test_size_keyword in test_size_keywords:
        no_of_concentrators = 0
        no_of_terminals = 0
        no_of_cycles_sa = 0
        no_of_iterations_sa = 0
        initial_temp_sa = 0
        final_temp_sa = 0
        concentrator_deployment_costs = []
        concentrator_capacities = []
        terminal_demands = []
        terminal_assigment_costs = []

        # Parsing the initialsetup.csv which holds the information on number of concentrators, and number of terminals in the network
        with open('TestData/Phase_1/' + data_directory_keyword + '/' + test_size_keyword + '/initialsetup.csv', encoding='utf8') as csvfile:
          readCSV = csv.reader(csvfile, delimiter=',')
          'The following line skips the row that includes the headers'
          next(readCSV)
          for row in readCSV:
              no_of_concentrators = int(row[0])
              no_of_terminals = int(row[1])
              no_of_cycles_sa = int(row[2])
              no_of_iterations_sa = int(row[3])
              initial_temp_sa = float(row[4])
              final_temp_sa = float(row[5])
        # Parsing the concentrator_capacity_initialcost.csv which holds the information on individual concentrator capacities, and deployment costs.
        with open('TestData/Phase_1/' + data_directory_keyword + '/' + test_size_keyword + '/concentrator_capacity_initialcost.csv', encoding='utf8') as csvfile:
          readCSV = csv.reader(csvfile, delimiter=',')
          next(readCSV)
          for row in readCSV:
                concentrator_capacities.append(int(row[0]))
                concentrator_deployment_costs.append(int(row[1]))
        # Parsing the terminal_demand_assigncost.csv which holds the information on individual individual terminal demands, and costs of the links with each one of the concentrators.
        with open('TestData/Phase_1/' + data_directory_keyword + '/' + test_size_keyword + '/terminal_demand_assigncost.csv', encoding='utf8') as csvfile:
          readCSV = csv.reader(csvfile, delimiter=',')
          next(readCSV)
          for row in readCSV:
                terminal_demands.append(int(row[0]))
                terminal_assigment_costs.append([int(x) for x in row[1].split("-")])


        # Simulated Annealing
        sa_running_times = []
        sa_costs = []
        sa_solutions = []
        sa_used = []
        sa_capacities = []
        for i in range(10):
          start_time = time.time()
          simulated_annealing = SimulatedAnnealing(concentrator_deployment_costs, concentrator_capacities, terminal_demands, terminal_assigment_costs, no_of_concentrators, no_of_terminals, no_of_cycles_sa, no_of_iterations_sa, final_temp_sa, initial_temp_sa, data_directory_keyword, test_size_keyword)
          simulated_annealing_cost, simulated_annealing_solution, simulated_annealing_used, simulated_annealing_concentrator_capacities = simulated_annealing.run()
          simulated_annealing_running_time = time.time() - start_time     
          sa_running_times.append(simulated_annealing_running_time)
          sa_costs.append(simulated_annealing_cost) 
          sa_solutions.append(simulated_annealing_solution)
          sa_used.append(simulated_annealing_used)
          sa_capacities.append(simulated_annealing_concentrator_capacities)

        # Calculate SA Properties
        sa_cost_min = min(sa_costs)
        sa_cost_min_index = sa_costs.index(sa_cost_min)
        sa_best_solution = sa_solutions[sa_cost_min_index]
        sa_best_used = sa_used[sa_cost_min_index]
        sa_best_capacities = sa_used[sa_cost_min_index]

        # Greedy
        start_time = time.time()
        greedy_cost, greedy_solution, greedy_used, greedy_concentrator_capacities = Greedy(concentrator_deployment_costs, concentrator_capacities, terminal_demands, terminal_assigment_costs, no_of_concentrators, no_of_terminals, data_directory_keyword, test_size_keyword)
        greedy_running_time = time.time() - start_time

        # Writing to file SA
        simulated_annealing_file = open('Results/Phase_1/' + data_directory_keyword + '/' + test_size_keyword + '/SimulatedAnnealing.txt', 'w')
        simulated_annealing_file.write('Algorithm ran on average: %s seconds' % (np.average(sa_running_times)) + '\n' + 
        'Algorithm ran on min: %s seconds' % (min(sa_running_times)) + '\n' + 
        'Algorithm ran on max: %s seconds' % (max(sa_running_times)) + '\n' + 
        'Algorithm\'s running time variance: %s seconds' % (np.var(sa_running_times)) + '\n' + 
        'Best Solution Network Cost:' + '\n' + str(sa_cost_min) + '\n' + 
        'Best Solution Concentrators Used:'+ '\n' + str(sa_best_used) + '\n' + 
        'Best Solution Concentrator Capacities:'+ '\n' + str(sa_best_capacities) + '\n' + 
        'Best Solution Terminal-Concentrator Relation: ' + '\n' + str(sa_best_solution))
        simulated_annealing_file.close()

        # Writing to file Greedy
        greedy_file = open('Results/Phase_1/' + data_directory_keyword + '/' + test_size_keyword + '/Greedy.txt', 'w')
        greedy_file.write('Algorithm ran in: %s seconds' % (greedy_running_time) + '\n' + 'Network Cost:' + '\n' + str(greedy_cost) + '\n' + 'Concentrators Used:'+ '\n' + str(greedy_used) + '\n' + 'Concentrator Capacities:'+ '\n' + str(greedy_concentrator_capacities) + '\n' + 'Terminal-Concentrator Relation: ' + '\n' + str(greedy_solution))
        greedy_file.close()