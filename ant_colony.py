import random
import copy as dc
import numpy as np

nodes = ['A', 'B', 'C', 'D', 'E']

default_pheromone= { # Use greedy approach to genereate t0, 
    'A' : 1,
    'B' : 1,
    'C' : 1,
    'D' : 1,
    'E' : 1
}

default_weight = {
    'A': 5,
    'B': 2,
    'C': 4,
    'D': 2,
    'E': 3
}

default_edges = {
    'A': ['B', 'E'],
    'B': ['A', 'C'],
    'C': ['B', 'D'],
    'D': ['C', 'E'],
    'E': ['A', 'D']  
}

default_connectivity = {
    'AB': 1 ,'AC': 0, 'AD': 0, 'AE': 1,
    'BC': 1, 'BD': 0, 'BE':0,
    'CD': 1, 'CE': 0,
    'DE': 1
}


cycles = 100
cSize = 3
#cycle evap rate
local_evaporation = 0.5

#global pheromone updating rul
global_evaporation = 0.9
expansion_value = 1.05


q0 = 0.2
#t0 = supposed to equal our greedy approach

def acomvc(pheromones:dict, connectivity: dict, cSize: int, q0: int, cycles: int, nodes: list, weight: dict, edges: dict): 
    gp = pheromones
    best_set = []
    best_weight = 99999
    
    
    for _ in range(cycles):
        cycle_pheromone = gp
        print('cycle_pheromone', cycle_pheromone)
        cycle = random.sample(nodes, cSize)
        best_cycle_weight = 99999
        best_cycle_set = []
        
        for tour in cycle:
            tour_pheromone = cycle_pheromone
            print('tour_pheromone', tour_pheromone)
            tour_set = [tour]
            tour_weight = weight[tour]
            tour_con = connectivity
            tour_con = update_con(tour_con, tour, edges)
            remaining_edges = evaluate_connectivity(tour_con)
            while remaining_edges != 0: 
                q = random.uniform(0,1)
                next_node = None
                if q <q0:
                    next_node = hueristic(tour_con, tour_pheromone)
                else:
                    next_node = pheromone(tour_pheromone, tour_con)
                
                #After we have determined which node to add to the tour set    
                tour_con = update_con(tour_con, next_node, edges)  
                tour_weight += default_weight[next_node]
                tour_set += next_node
                #tour_pheromone.pop(next_node)
        
                
                remaining_edges = evaluate_connectivity(tour_con)
              
            # after the tour    
            if tour_weight < best_cycle_weight:
                best_cycle_weight = tour_weight
                best_cycle_set = tour_set      
            
                
            for node in tour_set:
                new_pheromone_value = (1- local_evaporation) + cycle_pheromone[node] * local_evaporation #τi = (1 − ϕ)τi + ϕτ0
                cycle_pheromone.update({node: new_pheromone_value})   
        
         
             
           
        
        #After we complete a cycle
        if best_cycle_weight < best_weight:
            best_weight = best_cycle_weight
            best_set = best_cycle_set
    
        gp = {key: value * (1- global_evaporation) for key, value in gp.items()}
            #there is a decay rate that hits all of them regardless of being included in the best cycle set   eqation 11 == (1 − ρ)τi)
        for node in best_cycle_set:
            new_pheromone_value = gp[node] + 1/best_cycle_weight
            gp.update({node: new_pheromone_value})  
            # this will add pheromone to the nodes used in the best set
  
 
    return [sorted(best_set), best_weight]                
        
        
        
def update_con(passed_con:dict, node:str, edges:dict):  # this function was awful
    updated_con = dc.deepcopy(passed_con)
    changes = edges[node]  
    for c in changes:
        sorted_string = ''.join(sorted(node + c))
        updated_con[sorted_string] = 0                            
    return updated_con

def evaluate_connectivity(connectivity: dict):  # we are working here 
    unconnected = 0
    for values in connectivity.values():
        unconnected += values
    return unconnected    

def pheromone(pheromone:dict, connectivity: dict): 
    options = list(pheromone.keys())
    probabilities = [None] * len(options)
    for i in range(len(options)):
        cv = common_value(options[i], pheromone, connectivity)
        probabilities[i]= cv  
    denominator = sum(probabilities)    
    for p in range(len(probabilities)):
        probabilities[p] = probabilities[p]/denominator
    next_node = np.random.choice(options, size=1, p=probabilities) 
    return next_node[0]

def hueristic(connectivity:dict, pheromone:dict):        
    options = list(pheromone.keys()) 
    option_strength = []
    for node in options:
        option_strength.append(common_value(node, pheromone, connectivity))
    next_node = options[np.argmax(option_strength)] 
    return next_node[0]
        
def common_value(node: str, pheromone: dict, connectivity: dict):
    total_p_edges = 0
    p_edges = default_edges[node]
    for i in p_edges:
        for i in p_edges:
            edge = node + i
            edge = ''.join(sorted(edge))
            if connectivity[edge] == 1 :
                total_p_edges += 1
    value = pheromone[node] * total_p_edges/ default_weight[node]
    return value

def greedy(nodes: list, weight: dict, edges: dict, connectivity: dict):
    print('starting greedy')
    g_connectivity = dc.deepcopy(connectivity)
    greedy_set = []
    greedy_weight = 0
   
    # We first must find a value for every node in order to see what gives us the most connnectivity for it's weight. 
    # Large values are prioritized in being added to the set
    value_dict = {}
    
    def evaluate_value(node: str):
            node_edges = edges[node]
            total_p_edges = 0
            for e_node in node_edges:
                edge = e_node + node
                edge = ''.join(sorted(edge))
                if connectivity [edge] == 1:
                    total_p_edges +=1
            return (total_p_edges/ weight[node])
    
  
    # Iterating over every node once and adding the node + value to the value dict.
    for node in nodes:
        value_dict[node] = evaluate_value(node)
    print('value_dict initialized')
    print('connectivity is ', evaluate_connectivity(g_connectivity))
    while evaluate_connectivity(g_connectivity) != 0:
        # Find the node with the largest value and add it to the set. Update the total weight of the set. Then remove this node from the dictionary.
        next_node = max(value_dict, key = value_dict.get)
        greedy_set += next_node
        greedy_weight += weight[next_node]
        value_dict.pop(next_node)
        
        #update the connectivity
        g_connectivity = update_con(g_connectivity, next_node, edges)
        
        # We have to update the value for each node that was connected to the edges in 'next_node'
        print('connectivity is ', evaluate_connectivity(g_connectivity))
        for node in edges[next_node]:
            value_dict[node] = evaluate_value(node)
                
    return [greedy_set, greedy_weight]
                
            
        
        
 
            


# TODO: Clean up code 

# Run the code, make sure it actually runs
# Add the greedy function that returnes the t0 (default pheromones)
# add optimal solution algorithm to compare the result of the ACOMWVC to. 
# find ways to generate random graphs. Especially Erdos Renyi model. THis can be used to test our ACOMWVC algo. 



# Done

# make a seperate function that calculates the product of pheromone and the (potential edges/ weight). We use this in both the hueristic and the

# finish creating the example dictionaries

# hueristic function, pheromone function, both pheromone udating rules, fix spelling of pheromone, 

# fix spelling oh pheromone

# Run the code, make sure it actually runs

