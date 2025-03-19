import sample_ReBac as sr
import pattern_tracker as pt
import dict_to_csv as d2c
import networkx_to_csv as n2c
import rule_finder as rf
import hueristic_miner as hm
import hueristic_miner2 as hm2
import lla_csv
import networkx as nx
print('starting')

# Iterations is for hueristic_miner only
iterations = 1000

max_rule_length = 5
num_nodes = 1000
num_edges = 15000
# num_nodes = 1000
# num_edges = 20000
relationships = ['a', 'b', 'c', 'd', 'e']
rules = [
    ['a', 'b', 'c', 'd', 'e'],
    ['a', 'a', 'a', 'a', 'a'],
    ['e', 'd', 'c', 'b', 'a']
]
# Generating our graph or loading our graph
graph = sr.generate_graph(num_nodes, num_edges, relationships)
# graph = n2c.load_graph('graph.csv')
# lla = lla_csv.load_lla()
print('finished generating graph')

lla = sr.create_lla(graph)
lla = sr.grant_access(rules, lla, graph)
print('created lla')

# Tracking the present and missing relationship patterns
tracker = pt.Tracker(relations= relationships.copy(), max_depth=max_rule_length) # YOU MUST MANUALLY INPUT A THE RELATIONSHIPS, YOU CANNOT USE A LIST OF RELATIONSHIPS!!!! 
tracker.detect_pattern(graph)
missing = tracker.show_missing()
print('finished tracking')


# If a pattern is missing from the graph, we add nodes to represent them. 
# We could potentially add nodes to represent all patterns.
if missing:
    sr.update_graph(graph, missing, rules)
    lla = sr.create_lla(graph)
    lla = sr.grant_access(rules, lla, graph)

# Save files

# Implement algorithims to find policy under this line
# hm2.hueristic_miner(lla, max_rule_length, relationships.copy(), graph, iterations)

# Save files
# nx.write_gexf(graph, 'graph.gexf') 
# lla_csv.save_lla(new_lla, 'new_lla.csv')
# print(rf.find_policy(graph, max_rule_length, lla, relationships.copy()))

# Average time using this algo
avg_time = 0

for i in range(50):
    time = hm2.hueristic_miner(lla, max_rule_length, relationships.copy(), graph, iterations)
    print(f"Elapsed time: {time:.2f} seconds for iteration {i + 1}")
    avg_time += time
    

print(f'The average time the algorithm used was {avg_time/50:.2f} seconds')