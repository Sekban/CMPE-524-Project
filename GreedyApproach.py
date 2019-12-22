import copy

def Greedy(concentrator_costs, concentrator_capacities, terminal_demands, terminal_assignment_costs, no_of_concentrators, no_of_terminals, data_directory_keyword, test_size_keyword):
    network_solution = []
    concentrators_used = []
    network_cost = sum(concentrator_costs)
    original_concentrator_capacities = copy.deepcopy(concentrator_capacities)
    concentrator_capacities = copy.deepcopy(concentrator_capacities)
    for idx in range(no_of_terminals):
        terminal_demand = terminal_demands[idx]
        terminal_assignment_cost = terminal_assignment_costs[idx]
        # Forming a new dst which holds the terminal, and its corresponding assignment costs to concentrators
        terminal_assignment_costs_dst = []
        for i in range(no_of_concentrators):
            terminal_assignment_costs_dst.append((i, terminal_assignment_cost[i]))
        # Sorting the concentrator costs from the iterating terminal in an ascending order
        terminal_assignment_costs_dst.sort(key=lambda terminal_tuple: terminal_tuple[1])
        for terminal_tuple in terminal_assignment_costs_dst:
            # if the terminal's demand is less than the remaining capacity in the concentrator, the index of the container is added to the solution
            if concentrator_capacities[terminal_tuple[0]] >= terminal_demand:
                # The network solution list holds which which concentrator the indexed terminal is linked to.
                network_solution.append(terminal_tuple[0])
                # Respective concentrator's capacity is reduced by the terminal's demand
                concentrator_capacities[terminal_tuple[0]] -= terminal_demand
                # Total network cost is increased by the cost of the link
                network_cost += terminal_tuple[1]
                break
        
    for i in range(no_of_concentrators):
        # If a concentrator's capacity hasn't decreased, it means it's not being utilised. Hence we could deduct the cost related from the network cost.
        if concentrator_capacities[i] == original_concentrator_capacities[i]:
            network_cost -= concentrator_costs[i]
        
        if i in network_solution:
            concentrators_used.append(1)
        else:
            concentrators_used.append(0)
    return network_cost, network_solution, concentrators_used, concentrator_capacities
