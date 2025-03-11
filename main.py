import sample_ReBac as sr
import pattern_tracker as pt
import dict_to_csv as d2c
import networkx_to_csv as n2c
import rule_finder as rf
import hueristic_miner as hm
import hueristic_miner2 as hm2
# Iterations is for hueristic_miner only
iterations = 1000

max_rule_length = 5
num_nodes = 800
num_edges = 8000
relationships = ['a', 'b', 'c', 'd', 'e']
rules = [
    ['a', 'b', 'c', 'd', 'e'],
    ['a', 'a', 'a']

]
# Generating our graph
graph = sr.generate_graph(num_nodes, num_edges, relationships)
lla = sr.create_lla(graph)
lla = sr.grant_access(rules, lla, graph)

# Tracking the present and missing relationship patterns
tracker = pt.Tracker(relations= relationships.copy(), max_depth=3) # YOU MUST MANUALLY INPUT A THE RELATIONSHIPS, YOU CANNOT USE A LIST OF RELATIONSHIPS!!!! 
tracker.detect_pattern(graph)
missing = tracker.show_missing()


# If a pattern is missing from the graph, we add nodes to represent them. 
# We could potentially add nodes to represent all patterns.
if missing:
    sr.update_graph(graph, missing, rules)
    lla = sr.create_lla(graph)
    lla = sr.grant_access(rules, lla, graph)

d2c.dict_to_csv(lla)
n2c.save_graph(graph)

# Implement algorithims to find policy under this line
print('\n', '1st run')
new_lla = hm2.hueristic_miner(lla, max_rule_length, relationships.copy(), graph, iterations) 
print('\n', '2nd run')
test = hm2.hueristic_miner(new_lla, max_rule_length, relationships.copy(), graph, iterations) 
print('\n', '3rd run')
test2 = hm2.hueristic_miner(test, max_rule_length, relationships.copy(), graph, iterations) 
# hm.hueristic_miner(lla, max_rule_length, relationships.copy(), graph, iterations) 

# print(rf.find_policy(graph, max_rule_length, lla, relationships.copy()))
