import random
import copy as dc
import numpy as np
import networkx as nx
from itertools import product

q0 = 0.9 # rate at which we are selecting hueristic vs pheromone
cycles = 200
cSize = 10

# It seems if the evaporation rate is too high, the pheremones drop too low and
# you will get a negative value for probability
local_evaporation = 0.9
global_evaporation = 0.05
expansion_value = 1.05



def aco_mcv(graph : nx.classes.graph.Graph):
    global_graph = graph
    best_set = []
    best_weight = float('inf')
    
    for _ in range(cycles):
        cycle_graph = dc.copy(global_graph)
        cycle = random.sample(graph.nodes, cSize)
        best_cycle_weight = float('inf')
        best_cycle_set = []
        
        for tour in cycle:
            tour_graph = cycle_graph
            tour_set = [tour]
            # I think this was the problem ############
            tour_graph.nodes[tour]['selected'] = True ##########################
            tour_weight = graph.nodes[tour]['weight']
            remaining_edges = evaluate_connectivity(tour_graph)
            
            while remaining_edges != 0:
                q = random.uniform(0,1)
                next_node = None
               
                if q < q0: 
                    next_node = hueristic(tour_graph)
                    method_debug = 'hueristic'
                else:
                    next_node = pheromone(tour_graph)     
                 
                
                # if next_node == None: # Removed this, but I may need to add it back, not sure
                #     break
                
                # Flagging the selected node and it's neighbors    
                tour_graph.nodes[next_node]['selected'] = True
                for neighbor in tour_graph.neighbors(next_node):
                    tour_graph.nodes[neighbor]['selected'] = True
                
                # Adding the node to the tour set and weight   
                tour_weight += graph.nodes[next_node]['weight']  
             
                tour_set.append(next_node)
                
                # Checking if there is any nodes that are not connected by the set
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
    
    
    ## Return statement
    iv = []
    bss = sorted(best_set)
    for node in bss:
        iv.append(global_graph.nodes[node]['weight'])
    
    return['Best set is' ,sorted(best_set), 'Weight of individual nodes', iv, 'Best weight is:', best_weight, ]    
 
            
def generate_connected_erdos_renyi(s, p):
    while True:
        G = nx.erdos_renyi_graph(s, p) 
        if nx.is_connected(G):
            for n in G.nodes:
                G.nodes[n]['weight'] = random.randint(1,20)
                G.nodes[n]['pheromone'] = 1
                G.nodes[n]['selected'] = False
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
        

def hueristic(graph: nx.classes.Graph):
    s_node = None
    s_value = 0
    for node in graph:
        
        if graph.nodes[node]['selected'] == False:
            if s_value < common_value(node, graph):
                s_value = common_value(node, graph)
                s_node = node
    return s_node

def greedy(graph: nx.classes.Graph):
    g_set = []
    weight = 0
    
    complete = False
    while complete == False:
        
        nodes_in_graph = graph.number_of_nodes()
        for node in graph:
            if graph.nodes[node]['selected'] == False:
                break
            else:
                nodes_in_graph -= 1  
        if nodes_in_graph == 0:
            complete = True
        
        option_strength = []
        
        for node in graph:
            if graph.nodes[node]['selected'] == False: 
                p_nodes = 1
                for neighbor in graph.neighbors(node):
                        if graph.nodes[neighbor]['selected'] == False:
                            p_nodes += 1 
                strength = graph.nodes[node]['weight'] / p_nodes 
                option_strength.append(strength)
            else:
                option_strength.append(0)
        
        next_node_index = option_strength.index(max(option_strength))
        g_set.append(next_node_index)
        weight += graph.nodes[next_node_index]['weight']
        
        graph.nodes[next_node_index]['selected'] = True
        for neighbor in graph.neighbors(next_node_index):
            graph.nodes[neighbor]['selected'] = True
    return (g_set, weight)       


    
    