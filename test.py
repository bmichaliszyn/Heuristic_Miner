import sample_ReBac as sr
import pattern_tracker as pt
import dict_to_csv as d2c
import networkx_to_csv as n2c
import rule_finder as rf
import miscellaneous_sorted.hueristic_miner as hm
import hueristic_miner2 as hm2
import miscellaneous_sorted.hueristic_miner3 as hm3
import miscellaneous_sorted.heuristic_miner4 as hm4
# import hueristic_miner5 as hm5
import lla_csv
import networkx as nx
import random


# Iterations is for hueristic_miner only
iterations = 1000



def generate_rules(relationships, num_rules, max_rule_length):
    
    rules = []
    
    while len(rules) < num_rules:
        rule_length = random.randint(4, max_rule_length) # Randomly select a rule length between 4 and the number of relationships
        rule = [random.choice(relationships) for _ in range(rule_length)] 
        if rule not in rules:
            rules.append(rule)  
            
    return rules


attempts = 20
num_rules = 30
num_nodes = 1000
num_edges = 8000
max_rule_length = 5
relationships = ['a', 'b', 'c', 'd' ]

avg_time_lowtohigh = 0
avg_time_hightolow = 0
avg_time_none = 0
ls_lth = 0
ls_hl = 0
ls_none = 0
for i in range(attempts):
    print('\n\n\n')
    print(f'attempt {i + 1}')
    graph = sr.generate_graph(num_nodes, num_edges, relationships)
    rules = generate_rules(relationships, num_rules, max_rule_length)
    lla = sr.create_lla(graph)
    lla = sr.grant_access(rules, lla, graph)
    tracker = pt.Tracker(relations= relationships.copy(), max_depth=max_rule_length) # YOU MUST MANUALLY INPUT A THE RELATIONSHIPS, YOU CANNOT USE A LIST OF RELATIONSHIPS!!!! 
    tracker.detect_pattern(graph)
    missing = tracker.show_missing()
    print('finished tracking')
    if missing:
        sr.update_graph(graph, missing, rules)
        lla = sr.create_lla(graph)
        lla = sr.grant_access(rules, lla, graph)
        
    time, ls = hm2.hueristic_miner(lla, max_rule_length, relationships.copy(), graph, iterations)
    avg_time_lowtohigh += time
    ls_lth += ls
    time, ls = hm3.hueristic_miner(lla, max_rule_length, relationships.copy(), graph, iterations)
    avg_time_hightolow += time
    ls_hl += ls
    time, ls = hm4.hueristic_miner(lla, max_rule_length, relationships.copy(), graph, iterations)
    avg_time_none += time
    ls_none += ls
print('\n')
print(f'Low to high method time: {avg_time_lowtohigh / attempts}')
print(f'Low to high method avg lla: {ls_lth / attempts}')

print(f'High to low method time: {avg_time_hightolow / attempts}')
print(f'High to low method avg lla: {ls_hl / attempts}')

print(f'None method time: {avg_time_none / attempts}')
print(f'None method avg lla: {ls_none / attempts}')


# sig_rules, time = rf.find_policy(graph, max_rule_length, lla, relationships.copy())
# # Generating our graph or loading our graph
# graph = sr.generate_graph(num_nodes, num_edges, relationships)
# # graph = n2c.load_graph('graph.csv')
# # lla = lla_csv.load_lla()
# print('finished generating graph')

# lla = sr.create_lla(graph)
# lla = sr.grant_access(rules, lla, graph)
# print('created lla')

# # Tracking the present and missing relationship patterns
# tracker = pt.Tracker(relations= relationships.copy(), max_depth=max_rule_length) # YOU MUST MANUALLY INPUT A THE RELATIONSHIPS, YOU CANNOT USE A LIST OF RELATIONSHIPS!!!! 
# tracker.detect_pattern(graph)
# missing = tracker.show_missing()
# print('finished tracking')


# # If a pattern is missing from the graph, we add nodes to represent them. 
# # We could potentially add nodes to represent all patterns.
# if missing:
#     sr.update_graph(graph, missing, rules)
#     lla = sr.create_lla(graph)
#     lla = sr.grant_access(rules, lla, graph)

# Save files

# Implement algorithims to find policy under this line
# hm2.hueristic_miner(lla, max_rule_length, relationships.copy(), graph, iterations)

# Save files
# nx.write_gexf(graph, 'graph.gexf') 
# lla_csv.save_lla(new_lla, 'new_lla.csv')
# print(rf.find_policy(graph, max_rule_length, lla, relationships.copy()))

# Average time using this algo
