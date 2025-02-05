

import networkx as nx
import matplotlib.pyplot as plt
import random

# Parameters for the random graph
num_nodes = 3
num_edges =15

# Relationship types
relationships = ['a', 'b', 'c']

#Rules for the access control
rules = [
# ['a', 'b', 'c'],
# ['c', 'a'],
['b'],
['a'],
['c']
]

# Create a MultiDiGraph
multi_digraph = nx.MultiDiGraph()

# Add nodes
multi_digraph.add_nodes_from(range(num_nodes))

# Add random edges (with multiple edges allowed)
while num_edges > 0:
    source, target = random.sample(range(num_nodes), 2)
    # Check if an edge already exists between the source and target that contains the same relationship
    taken = [] # List to store the types of relationships that have been taken

    # print('source:', source, 'target:', target)
    
    # Grab the edge data for the current edge, includes all edges!
    cur_edge_data = multi_digraph.get_edge_data(source, target)
    try:
        for i in cur_edge_data:
            taken.append(cur_edge_data[i]['type'])
    except: 
        pass

    # print('taken:', taken)
    
    potential_relationships = [x for x in relationships if x not in taken]   
    # print('potential relationships:', potential_relationships)

    if len(potential_relationships) > 0:
        relationship = random.choice(potential_relationships)  # Choose a random relationship type  
        multi_digraph.add_edge(source, target, type=relationship)
        num_edges -= 1

# Creating a dicitonary to store the node access control
lla_dict = {}
nodes = multi_digraph.nodes()
for node in nodes:
    lla_dict[node] = {}



def grant_access(node: int, rule: list, depth: int, original_node: int):
        # If we reach the end of the rule, we can grant access
        if len(rule) == depth:
            lla_dict[original_node][node] = True
            return
        # Grab the edges of the current node
        edges = multi_digraph.edges(node)
        
        # Create a list to store the next nodes
        next_nodes = set()
        for edge in edges:
            next_nodes.add(edge[1])
        
        for next_node in next_nodes:    
    
            # Remember, this grabs the edge data for the every edge, essentially we will retrieve all types of relationships
            edge_data = multi_digraph.get_edge_data(node, next_node)
            
            if edge_data:
                type = [x['type'] for x in edge_data.values()]
            else:
                type = []
            
            # If the edge type matches the rule, we can continue
            if rule[depth] in type:
                grant_access(next_node, rule, depth + 1, original_node)
                
            # If the edge type does not match the rule, we can't grant access
            else:
                return

# We need to apply the rules to each node

for node in nodes:
    for rule in rules:
        grant_access(node, rule, 0, node)

node_keys = list(lla_dict.keys())

# print the access control for each node
for node in node_keys:
    print('\n')
    print(node, 'has access to', lla_dict[node])

print('\n')
for node in nodes:
    
    # We are grabbing the out edges of the node
    edges = multi_digraph.edges(node)
    print('\n')
    print(node, 'has', len((list(edges))), 'edges')
    
    
    for source, target, key in multi_digraph.edges(node, keys=True):
        edge_data = multi_digraph.get_edge_data(source, target, key)  # Get data for specific edge
        
        # Print details correctly
        print(f'source={source}, target={target}, type={edge_data["type"]}')


# Print the number of edges and nodes
print('\n')
print('this graph contains', multi_digraph.number_of_edges(), 'edges')       
print('this graph contains', multi_digraph.number_of_nodes(), 'nodes')

# Visualize the MultiDiGraph
# pos = nx.spring_layout(multi_digraph)
# plt.figure(figsize=(8, 6))
# nx.draw(multi_digraph, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=700, arrowsize=20)
# edge_labels = nx.get_edge_attributes(multi_digraph, 'relationship')
# nx.draw_networkx_edge_labels(multi_digraph, pos, edge_labels=edge_labels)    
# plt.title("Random MultiDiGraph with Multiple Edges and Relationships")
# plt.show()

