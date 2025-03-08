import sample_ReBac as sr
import pattern_tracker as pt
import dict_to_csv as d2c
import networkx_to_csv as n2c
import rule_finder as rf

num_nodes = 6
num_edges = 20
relationships = ['a', 'b', 'c']
rules = [
    ['a', 'b', 'c']
]
# Generating our graph
graph = sr.generate_graph(num_nodes, num_edges, relationships)
lla = sr.create_lla(graph)
lla = sr.grant_access(rules, lla, graph)

# Tracking the present and missing relationship patterns
tracker = pt.Tracker(relations= relationships.copy(), max_depth=3) # YOU MUST MANUALLY INPUT A THE RELATIONSHIPS, YOU CANNOT USE A LIST OF RELATIONSHIPS!!!! PYTHON IS VERY BROKEN
tracker.detect_pattern(graph)
missing = tracker.show_missing()
print(len(missing),'sabongus')

# If a rule is missing from the graph, we add nodes to represent them. 
# We could potentially add nodes to represent all patterns.
if missing:
    sr.update_graph(graph, missing, rules)
    lla = sr.create_lla(graph)
    lla = sr.grant_access(rules, lla, graph)
    print('Rules were missing, added nodes and updated lla', graph)

d2c.dict_to_csv(lla)
n2c.save_graph(graph)

rf.find_policy(graph, 3, lla, relationships.copy())
grants = 0
for node in lla.keys():
    n_dict = lla[node]
    other_nodes = n_dict.keys()
    for o_n in other_nodes:
        if n_dict[o_n] == True:
            grants += 1
    

