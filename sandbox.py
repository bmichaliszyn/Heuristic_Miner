import networkx as nx

def generate_connected_erdos_renyi(n, p):
    """Generates a connected Erdos-Renyi graph with n nodes and edge probability p."""
    while True:
        G = nx.erdos_renyi_graph(n, p)
        if nx.is_connected(G):
            return G
        else:
            print('bad graph')

# Generate the graph
graph = generate_connected_erdos_renyi(100, 0.03)

# Find the node with the highest identifier
max_node = max(graph.nodes)

print(f"The node with the highest identifier is: {max_node}")

