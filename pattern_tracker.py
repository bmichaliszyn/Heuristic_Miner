# The use of this class is detect if there is a pattern present in the graph
# This tracker does not care whether or not access is granted or not, it only 
# cares if the pattern is present

import networkx as nx

class Tracker:
    def __init__(self, relations: list, max_depth: int):
        self.patterns = {}
        
        self.relations = relations
        self.max_depth = max_depth
        depth = 1
        while depth < self.max_depth :
            for rp in self.relations:
                if len(rp) == depth:
                    self.relations.append(rp + 'a')
                    self.relations.append(rp + 'b') 
                    self.relations.append(rp + 'c')
            depth += 1
        
        for rp in self.relations:
            self.patterns[rp] = False
        

    def show_size(self):
        print(len(self.relations))
    
    def show_missing(self):
        present = 0
        missing = 0
        for pattern in self.patterns.keys():
            if self.patterns[pattern] == False:
                 missing += 1
            else:
                present += 1
        print('Present:', present)
        print('Missing:', missing)
    
    def detect_pattern(self, graph: nx.MultiGraph):
        nodes = graph.nodes()
        
        
                
        def pattern_search(node: int, pattern: str, depth: int):
            if depth == self.max_depth:
                return
            next_nodes = graph.neighbors(node)
        
            for next_node in next_nodes:
                print(next_node)
                next_node_data = graph.get_edge_data(node, next_node)
    
                print('nnd 1', next_node_data)
                # print ('nnd 2', next_node_data[0]['type'])
    
                # for type in next_node_data:
                    
                 
                #     next_node_data = next_node_data[type]
                #     pattern = pattern + type
                #     self.patterns[pattern] = True
                # pattern_search(next_node, pattern, depth + 1)
        
        # For each node in the graph, we will perform a search for patterns
        for node in nodes:
            pattern_search(node, '', 0)
    
