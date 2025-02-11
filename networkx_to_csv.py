import networkx as nx
import csv

# It's actually faster to go through and save the edges
def save_graph(graph: nx.multidigraph, filename='graph.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        edges = graph.edges()
        for e in edges:
            edge_data = graph.get_edge_data(e[0],e[1])
            types = [x['type'] for x in edge_data.values()]
            writer.writerow([e[0]] + [e[1]] + types)
    return        


def load_graph(filename: str) -> nx.multidigraph:
    with open(filename, mode='r') as f:
        
        #Getting the edge data from the csv file
        reader = csv.reader(f)
        data = [edge for edge in reader]
        md_graph = nx.MultiDiGraph()

        for edge in data:
            source = int(edge[0])
            target = int(edge[1])
            
            # edge[2:] contains all of the relationship types
            types = edge[2:]
            
            # For each type, add an edge between source and target with type: type
            for t in types:
                md_graph.add_edge(source, target, t)   
    return md_graph

