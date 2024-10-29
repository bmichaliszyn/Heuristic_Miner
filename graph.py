import networkx as nx
import random
import matplotlib.pyplot as plt

# This will generate a graph where all nodes are connected to each other by a single edge. No node
# exists with out being connected to another. For example, because we have 10 nodes, we have 10 + (10 + 1)/2.
# Number of edges will be S_n of the first n integers. Expressed n + (n+1)/2
G = nx.complete_graph(15)
print('Graph generated has:', len(G.edges), 'edges.')

#Names of the nodes:
# for node in G.nodes:
#     print(node)


#Assigning weight: The following will give an attribute 'weight' to each node with values between 1 - 10. LV is 1 HV is 10
for n in G.nodes:
    G.nodes[n]['weight'] = random.randint(1,10)


# How to print weights of nodes    
# for n in G.nodes:
#     print(G.nodes[n]['weight'])

#Names of the edges: The edges are simply tuples.
# for edge in G.edges:
#     print(edge)

# Visual for the graph
nx.draw(G)
plt.show()
print('done')

