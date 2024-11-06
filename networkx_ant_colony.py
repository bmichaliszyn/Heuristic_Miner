import random
import copy as dc
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

s = 100 # Size of the graph
p = 0.03 # Proabability of connectedness 
q0 = 0.2 #rate at which we are selecting hueristic vs pheromone
cycles = 100
cSize = 3
local_evaporation = 0.5

global_evaporation = 0.9
expansion_value = 1.05



def aco_mcv(graph : nx.classes.graph.Graph):
    global_graph = graph
    best_set = []
    best_weight = 9999
    
    for _ in range(cycles):
        cycle_graph = global_graph
        cycle = random.sample(graph.nodes)
        best_cycle_weight = 9999
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
                    next_node = hueristic()###
                else:
                    next_node = pheromone() ###  
                # Need to update connectivity (selected)    
                tour_weight += graph.nodes[next_node]['weight']    
                remaining_edges = evaluate_connectivity(tour_graph)
                
            #after the tour    
            if tour_weight < best_cycle_weight:
                best_cycle_weight = tour_weight
                best_cycle_set = tour_set
            
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
    
    return[sorted(best_set), best_weight]        
            
            
def generate_connected_erdos_renyi(s, p):
    """Generates a connected Erdos-Renyi graph with n nodes and edge probability s."""
    """ while True: looks for a return statement or break """
    while True:
        G = nx.erdos_renyi_graph(s, p) 
        if nx.is_connected(G):
            return G
                
def evaluate_connectivity(graph: nx.classes.graph.Graph):
    return sum(1 for node in graph.nodes if graph.nodes[node].get('selected') == False)

def hueristic(graph: nx.classes.Graph): ######## WORKING HERE
    s_node = None
    s_value = 0
    for node in graph:
        if graph.nodes[node]['seleted'] == False:
            cur = graph.nodes[node]
            if s_value < common_value(cur):
                s_value = common_value(cur)
                s_node = cur
    return s_node

def pheromone(): 
    return None #TODO

def common_value(node, graph: nx.classes.Graph): ####
    cur = graph.nodes[node]
    edges = 0
    for neighbor in graph.neighbors(node):
        if graph.nodes[neighbor]['selected'] == False:
            edges += 1
    value = cur['pheromone'] * edges/cur['weight']    
    return value   
    


def main():
    graph = generate_connected_erdos_renyi(s,p)            
    
    for n in graph.nodes:
        graph.nodes[n]['weight'] = random.randint(1,10)
        graph.nodes[n]['pheromone'] = 1
        graph.nodes[n]['selected'] = False
    
    print(evaluate_connectivity(graph))    
    # nx.draw(graph)
    # plt.show()
    
    
   

main()    