import random
import copy
import math
import numpy as np


class SimulatedAnnealing:
    def __init__(self, concentrator_costs, concentrator_capacities, terminal_demands, terminal_assignment_costs, no_of_concentrators, no_of_terminals):
        self.network_solution = []
        self.network_cost = 0.0
        self.no_of_concentrators = no_of_concentrators
        self.no_of_terminals = no_of_terminals
        self.concentrator_costs = copy.deepcopy(concentrator_costs)
        self.original_concentrator_capacities = copy.deepcopy(concentrator_capacities)
        self.concentrator_capacities = copy.deepcopy(concentrator_capacities)
        self.terminal_demands = copy.deepcopy(terminal_demands)
        self.terminal_assignment_costs = copy.deepcopy(terminal_assignment_costs)
    
    # This method creates a preliminary solution in which the terminal demands are simply checked against randomly selected concentrators.
    def get_initial_solution(self):  
        index = 0
        while len(self.network_solution) < self.no_of_terminals:
            random_concentrator_index = random.randint(0, self.no_of_concentrators - 1)
            if self.concentrator_capacities[random_concentrator_index] >= self.terminal_demands[index]:
                if not random_concentrator_index in self.network_solution:
                    self.network_cost += self.concentrator_costs[random_concentrator_index]
            self.network_solution.append(random_concentrator_index)
            self.concentrator_capacities[random_concentrator_index] -= self.terminal_demands[index]
            self.network_cost += self.terminal_assignment_costs[index][random_concentrator_index]
            # index is incremented by 1 to be able to loop through all of the terminals
            index += 1
    
    def get_new_solution(self):
        solution = copy.deepcopy(self.network_solution)
        if random.randint(0,1) == 0:
            # We choose a random terminal index
            random_terminal_index = random.randint(0, self.no_of_terminals - 1)
            # We choose a random concentrator index
            random_concentrator_index = random.randint(0, self.no_of_concentrators - 1)
            flag = True
            for i in range(self.no_of_concentrators):
                # If any concentrator has a capacity that's higher than the demand of the randomly chosen terminal, the flag is set to false
                if self.concentrator_capacities[i] > self.terminal_demands[random_terminal_index]:
                    flag = False
                    break
            if flag:
                # If no concentrator is found to have a higher capacity than the randomly chosen terminal, we return back the solution, and the network cost.
                return solution, self.network_cost
            while self.concentrator_capacities[random_concentrator_index] - self.terminal_demands[random_terminal_index] < 0:
                # If the terminal demand concatenated away from the concentrator capacity leads to a negative value, we choose another random concentrator, and try to find a solution until one is found.
                random_concentrator_index = random.randint(0, self.no_of_concentrators - 1)
            solution[random_terminal_index] = random_concentrator_index
        else:
            # We choose two random terminal indexes
            random_terminal_index_1 = random.randint(0, self.no_of_terminals - 1)
            random_terminal_index_2 = random.randint(0, self.no_of_terminals - 1)
            # if both of the terminals are connected to the same concentrator, or either one of the terminals' concentrator capacity added with its own demand is less than the other one's demand, the indexes are regenerated and the whole procedure is ran again.
            while self.network_solution[random_terminal_index_1] == self.network_solution[random_terminal_index_2] or \
            self.concentrator_capacities[solution[random_terminal_index_2]] + self.terminal_demands[random_terminal_index_2] < self.terminal_demands[random_terminal_index_1] or \
            self.concentrator_capacities[solution[random_terminal_index_1]] + self.terminal_demands[random_terminal_index_1] < self.terminal_demands[random_terminal_index_2]:
                random_terminal_index_1 = random.randint(0, self.no_of_terminals - 1)
                random_terminal_index_2 = random.randint(0, self.no_of_terminals - 1)
            # If none of the conditions are met, we do a swap of the assigned concentrators of the terminals.
            solution[random_terminal_index_1], solution[random_terminal_index_2] = solution[random_terminal_index_2], solution[random_terminal_index_1]
            # Bear in mind the concentrator capacities are calculated after these steps.
        new_cost = 0
        for i in range(self.no_of_concentrators):
            if i in solution:
                new_cost += self.concentrator_costs[i]
        for i in range(self.no_of_terminals):
            new_cost += self.terminal_assignment_costs[i][solution[i]]
        return solution, new_cost

    def run(self):
        self.get_initial_solution()
        # 50 cycles for the size of this network
        no_of_cycles = 50
        # 500 iterations per cycle for the size of this network
        no_of_iterations = 500
        # Initial temperature, based on probability of accepting new solutions at the start
        t1 = -1.0/math.log(0.7)
        # Final temperature, based on probability of accepting new solutions at the end
        t50 = -1.0/math.log(0.001)
        # Fractional reduction every cycle
        frac = (t50/t1)**(1.0/(no_of_cycles-1.0))
        # Current temperature
        T = t1
        
        for i in range(no_of_cycles):
            for i in range(no_of_iterations):
                new_solution, new_cost = self.get_new_solution()
                if new_cost < self.network_cost:
                    # If a new solution yields a lower network cost than the existing one, we deepcopy the new solution, update the total cost, and concentrator capacities accordingly.
                    self.network_solution = copy.deepcopy(new_solution)
                    self.network_cost = new_cost
                    self.concentrator_capacities = copy.deepcopy(self.original_concentrator_capacities)
                    for i in range(self.no_of_terminals):
                        self.concentrator_capacities[self.network_solution[i]] -= self.terminal_demands[i]
                else:
                    # If the new solution's outcome isn't better than the previous iteration, the positive difference is calculated between the new network cost and the reigning one.
                    delta = new_cost - self.network_cost
                    # generate probability of acceptance
                    probability = np.exp(-delta / T)
                    # if the generated probability is higher than the generated random number, we accept the worse solution
                    if probability > random.random():
                        self.network_solution = copy.deepcopy(new_solution)
                        self.network_cost = new_cost
                        self.concentrator_capacities = copy.deepcopy(self.original_concentrator_capacities)
                        for i in range(self.no_of_terminals):
                            self.concentrator_capacities[self.network_solution[i]] -= self.terminal_demands[i]
            T *= frac
        concentrators_used = []
        for i in range(self.no_of_concentrators):
            if i in self.network_solution:
                concentrators_used.append(1)
            else:
                concentrators_used.append(0)
        return self.network_cost, self.network_solution, concentrators_used, self.concentrator_capacities

    