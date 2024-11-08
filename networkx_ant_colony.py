import random
import copy as dc
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

s = 100 # Size of the graph
p = 0.03 # Proabability of connectedness 
q0 = 0.9 # rate at which we are selecting hueristic vs pheromone
cycles = 100
cSize = 10

# It seems if the evaporation rate is too high, the pheremones drop too low and
# you will get a negative value for probability
local_evaporation = 0.9
global_evaporation = 0.05
expansion_value = 1.05



def aco_mcv(graph : nx.classes.graph.Graph):
    global_graph = graph
    best_set = []
    best_weight = 9999
    
    for _ in range(cycles):
        cycle_graph = global_graph.copy()
        cycle = random.sample(graph.nodes, cSize)
        best_cycle_weight = 99999
        best_cycle_set = []
        
        for tour in cycle:
            tour_graph = cycle_graph
            tour_set = [tour]
            tour_weight = graph.nodes[tour]['weight']
            remaining_edges = evaluate_connectivity(tour_graph)
            
            while remaining_edges != 0:
                q = random.uniform(0,1)
                next_node = None
                if q < q0: 
                    next_node = hueristic(tour_graph)
                else:
                    next_node = pheromone(tour_graph)     
                
                if next_node == None:
                    break
                # Flagging the selected node and it's neighbors    
                tour_graph.nodes[next_node]['selected'] = True
                for neighbor in tour_graph.neighbors(next_node):
                    tour_graph.nodes[neighbor]['selected'] = True
                   
                tour_weight += graph.nodes[next_node]['weight']  
                tour_set.append(next_node)
                remaining_edges = evaluate_connectivity(tour_graph)
            
            # After the tour
            
            # Reset the flag
            for node in cycle_graph.nodes:
                cycle_graph.nodes[node]['selected'] = False 

            #update best cycle weight and set 
            if tour_weight < best_cycle_weight:
                best_cycle_weight = tour_weight
                best_cycle_set = tour_set
                
            # Apply the pheromone changes 
            for node in tour_set:
                cycle_graph.nodes[node]['pheromone'] = (1- local_evaporation) + cycle_graph.nodes[node]['pheromone'] * local_evaporation
            
        # After a cycle
        if best_cycle_weight < best_weight:
            best_weight = best_cycle_weight
            best_set = best_cycle_set
        
        # General decay
        for node in global_graph.nodes:
            global_graph.nodes[node]['pheromone'] = global_graph.nodes[node]['pheromone'] * (1 - global_evaporation)    
        
        # Increasing selected nodes
        for node in best_cycle_set:
            global_graph.nodes[node]['pheromone'] = global_graph.nodes[node]['pheromone'] + 1/best_cycle_weight
    
    return['Best set is' ,sorted(best_set), 'Best weight is:', best_weight]        
            
            
def generate_connected_erdos_renyi(s, p):
    """Generates a connected Erdos-Renyi graph with n nodes and edge probability s."""
    """ while True: looks for a return statement or break """
    while True:
        G = nx.erdos_renyi_graph(s, p) 
        if nx.is_connected(G):
            return G
                
def evaluate_connectivity(graph: nx.classes.graph. Graph):
    return sum(1 for node in graph.nodes if graph.nodes[node].get('selected') == False)

def common_value(node: int, graph: nx.classes.Graph): #### I want to check this out again
    cur = graph.nodes[node]
    edges = 1
    for neighbor in graph.neighbors(node):
        if graph.nodes[neighbor]['selected'] == False:
            edges += 1    
    value = cur['pheromone'] * edges/cur['weight']    
    return value
    

def pheromone(graph: nx.classes.Graph): 
    
    options = list(range(graph.number_of_nodes())) 
    probabilities = []
    for node in graph:
        if graph.nodes[node]['selected'] == False:
            probabilities.append(common_value(node, graph)) 
        else:
            probabilities.append(0)
            
    denominator = sum(probabilities)   
    if denominator == 0:
        for node in graph.nodes:
             if graph.nodes[node]['selected'] == False:
                 print (common_value(node, graph))
    for p in range(len(probabilities)):
        probabilities[p] = probabilities[p]/denominator
        
    next_node = np.random.choice(options, size = 1, p = probabilities)[0]   
    return next_node
        

def hueristic(graph: nx.classes.Graph): ######## WORKING HERE
    s_node = None
    s_value = 0
    for node in graph:
        
        if graph.nodes[node]['selected'] == False:
            if s_value < common_value(node, graph):
                s_value = common_value(node, graph)
                s_node = node
    return s_node

   
    
