import ant_colony as ac



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


cycles =3
cSize =5
#cycle evap rate
local_evaporation = 0.5

#global pheromone updating rul
global_evaporation = 0.9
expansion_value = 1.05


q0 = 0.2
# #t0 = supposed to equal our greedy approach
# print(ac.acomvc(default_pheromone, default_connectivity, cSize, q0, cycles, nodes, default_weight, default_edges))
# nodes: list, weight: dict, edges: dict, connectivity: dict
print(ac.greedy(nodes, default_weight, default_edges, default_connectivity))



#####################################################################################################
# The following can be used to determine which nodes will be selected in the greedy approach. After
# determining the nodes, we update the pheremones with an increase of favorability
t0 = (ac.greedy(nodes, default_weight, default_edges, default_connectivity))[0]
print(t0)
C = (ac.greedy(nodes, default_weight, default_edges, default_connectivity))[1]

for node in t0:
    default_pheromone[node] = (len(nodes) * (len(nodes)-len(t0)) / C)

print(default_pheromone)
######################################################################################################