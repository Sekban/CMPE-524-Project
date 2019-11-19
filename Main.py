import csv
import math
import time
from GreedyApproach import Greedy
from SimulatedAnnealing import SimulatedAnnealing

no_of_concentrators = 0
no_of_terminals = 0
concentrator_deployment_costs = []
concentrator_capacities = []
terminal_demands = []
terminal_assigment_costs = []

if __name__ == "__main__":
  # Parsing the initialsetup.csv which holds the information on number of concentrators, and number of terminals in the network
  with open('TestData/initialsetup.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    'The following line skips the row that includes the headers'
    next(readCSV)
    for row in readCSV:
        no_of_concentrators = int(row[0])
        no_of_terminals = int(row[1])
  # Parsing the concentrator_capacity_initialcost.csv which holds the information on individual concentrator capacities, and deployment costs.
  with open('TestData/concentrator_capacity_initialcost.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for row in readCSV:
          concentrator_capacities.append(int(row[0]))
          concentrator_deployment_costs.append(int(row[1]))
  # Parsing the terminal_demand_assigncost.csv which holds the information on individual individual terminal demands, and costs of the links with each one of the concentrators.
  with open('TestData/terminal_demand_assigncost.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for row in readCSV:
          terminal_demands.append(int(row[0]))
          terminal_assigment_costs.append([int(x) for x in row[1].split("-")])


  # Simulated Annealing
  start_time = time.time()
  simulated_annealing = SimulatedAnnealing(concentrator_deployment_costs, concentrator_capacities, terminal_demands, terminal_assigment_costs, no_of_concentrators, no_of_terminals)
  simulated_annealing_cost, simulated_annealing_solution, simulated_annealing_used, simulated_annealing_concentrator_capacities = simulated_annealing.run()
  simulated_annealing_running_time = time.time() - start_time

  # Greedy
  start_time = time.time()
  greedy_cost, greedy_solution, greedy_used, greedy_concentrator_capacities = Greedy(concentrator_deployment_costs, concentrator_capacities, terminal_demands, terminal_assigment_costs, no_of_concentrators, no_of_terminals)
  greedy_running_time = time.time() - start_time

  greedy_file = open('Results/Greedy.txt', 'w')
  greedy_file.write('Algorithm ran in: %s seconds' % (greedy_running_time) + '\n' + 'Network Cost:' + '\n' + str(greedy_cost) + '\n' + 'Concentrators Used:'+ '\n' + str(greedy_used) + '\n' + 'Concentrator Capacities:'+ '\n' + str(greedy_concentrator_capacities) + '\n' + 'Terminal-Concentrator Relation: ' + '\n' + str(greedy_solution))
  greedy_file.close()

  simulated_annealing_file = open('Results/SimulatedAnnealing.txt', 'w')
  simulated_annealing_file.write('Algorithm ran in: %s seconds' % (simulated_annealing_running_time) + '\n' + 'Network Cost:' + '\n' + str(simulated_annealing_cost) + '\n' + 'Concentrators Used:'+ '\n' + str(simulated_annealing_used) + '\n' + 'Concentrator Capacities:'+ '\n' + str(simulated_annealing_concentrator_capacities) + '\n' + 'Terminal-Concentrator Relation: ' + '\n' + str(simulated_annealing_solution))
  simulated_annealing_file.close()
  