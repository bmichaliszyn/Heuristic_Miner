import networkx as nx
import random
from typing import List

def generate_graph(num_nodes: int, num_edges:int, relationships: list[str]):
    # Parameters for the random graph

    # num_edges can equal up to N where N is the number of nodes in the graph 
    # (N(N-1))/2 * R where R is the number of relationships
    
    # Creating a tracker object for metadata
    #tracker = pt.Tracker(relations= relationships.copy(), max_depth=3) # YOU MUST MANUALLY INPUT A THE RELATIONSHIPS, YOU CANNOT USE A LIST OF RELATIONSHIPS!!!! PYTHON IS VERY BROKEN

    # Create a MultiDiGraph
    multi_digraph = nx.MultiDiGraph()

    # Add nodes
    multi_digraph.add_nodes_from(range(num_nodes))

    # Add random edges (with multiple edges allowed)
    while num_edges > 0:
        source, target = random.sample(range(num_nodes), 2)
        # Grab the edge data for the current edge, includes all edges!
        cur_edge_data = multi_digraph.get_edge_data(source, target)
        taken = [] # List to store the types of relationships that have been taken
        try:
            for i in cur_edge_data:
                type_string = (cur_edge_data[i]['type'])
                for c in type_string:
                    taken.append(c)
        except: 
            pass
        potential_relationships = [x for x in relationships if x not in taken]   

        if len(potential_relationships) > 0:
            relationship = random.choice(potential_relationships)  # Choose a random relationship type  
            multi_digraph.add_edge(source, target, type=relationship)
            num_edges -= 1
    return multi_digraph

# Creating a dicitonary to store the node access control
def create_lla(some_graph: nx.Graph) -> dict:
    lla_dict = {}
    nodes = some_graph.nodes()
    for node in nodes:
        lla_dict[node] = {}
        for i in range(len(nodes)):
            lla_dict[node][i] = False
    return lla_dict


def grant_access(rules: list, lla_dict: dict, graph: nx.Graph):
     
    def check_rule(node: int, path: List[int], original_node:int, depth: int, rule: List[str]):
        # If we reach the end of the rule, we can grant access #Make sure node != original_node
        if len(rule) == depth:
            new_lla[original_node][node] = True
            return
    
        
        for next_node in graph.neighbors(node):
            if next_node in path:
                continue
        
            # Remember, this grabs the edge data for the every edge, essentially we will retrieve all types of relationships
            edge_data = graph.get_edge_data(node, next_node)
            types = [x['type'] for x in edge_data.values()] if edge_data else []
        
                # From the node we're looking at to the next node, we are keeping track of existing relationships bewteen the two nodes (outgoing)
            
            # If the edge type matches the rule, we can continue
            if rule[depth] in types:
                check_rule(next_node, path + [next_node], original_node, depth + 1, rule)
                
    new_lla = lla_dict
    for node in graph.nodes(): 
        for rule in rules:
            check_rule(node, [node], node, 0, rule)
        
    return new_lla

        

# We need to apply the rules to each node

# for node in nodes:
#     for rule in rules:
#         grant_access(node, rule, 0, node, [])

# node_keys = list(lla_dict.keys())




#Print the number of edges and nodes

# print('this graph contains', multi_digraph.number_of_edges(), 'edges')       
# print('this graph contains', multi_digraph.number_of_nodes(), 'nodes')

# Visualize the MultiDiGraph

# pos = nx.spring_layout(multi_digraph)
# plt.figure(figsize=(8, 6))
# nx.draw(multi_digraph, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=700, arrowsize=20)
# edge_labels = nx.get_edge_attributes(multi_digraph, 'relationship')
# nx.draw_networkx_edge_labels(multi_digraph, pos, edge_labels=edge_labels)    
# plt.title("Random MultiDiGraph with Multiple Edges and Relationships")
# plt.show()


# tracker.detect_pattern(multi_digraph)
# tracker.show_size()

def update_graph(graph: nx.Graph, missing: List[list], rules):

    new_nodes = []
    # Add the missing patterns to the graph, if it is a rule
    for m in missing:
        
        # I can comment this out if I want to add all missing patterns
        
        # if list(m) not in rules:
        #     continue
        
        #print('adding nodes to represent rule:', list(m))
        # The next node id is the length of the nodes in the graph
        node_id = len(graph.nodes) 
        start = node_id
        
        # Take each edge and store the values of the relationships in a list
        edges = list(m)
        
        # Adding new nodes to graph to create the missing pattern
        for _ in range(len(edges) + 1):
            graph.add_node(node_id)
            new_nodes.append(node_id)
            node_id += 1
        
        # Adding edges to the graph to create the missing pattern
        
        for i in range(len(edges)):  
            graph.add_edge(start, start + 1, type=edges[i])
            start += 1




# nodes = multi_digraph.nodes()
# for node in nodes:
#     lla_dict[node] = {}
#     for i in range(len(nodes)):
#         lla_dict[node][i] = False

# for node in nodes:
#     for rule in rules:
#         grant_access(node, rule, 0, node, [])


# # Save the low level access control to a csv file
# d2c.dict_to_csv(lla_dict)

# # Save the graph to a csv file

# n2c.save_graph(multi_digraph, 'graph.csv')    

# print(multi_digraph)


# # We now have a graph that contains all possible patterns given a length N

# # import rule_finder as rf

# # print(rf.find_policy(multi_digraph, 3, lla_dict, relationships))

# # print the access control for each node
# # for node in node_keys:
# #     print('\n')
# #     print(node, 'has access to', lla_dict[node])

# print('\n')
# for node in nodes:
    
#     # We are grabbing the out edges of the node
#     edges = multi_digraph.edges(node)
#     print('\n')
#     print(node, 'has', len((list(edges))), 'edges')
    
    
#     for source, target, key in multi_digraph.edges(node, keys=True):
#         edge_data = multi_digraph.get_edge_data(source, target, key)  # Get data for specific edge
        
#         # Print details correctly
#         print(f'source={source}, target={target}, type={edge_data["type"]}')