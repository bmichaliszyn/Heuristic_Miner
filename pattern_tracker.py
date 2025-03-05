# The use of this class is detect if there is a pattern present in the graph
# This tracker does not care whether or not access is granted or not, it only 
# cares if the pattern is present

import networkx as nx

class Tracker:
    def __init__(self, relations: list, max_depth: int):
        
        # Thank you Chat GPT for helping me with this
        # Why Your Code Breaks
        # If Tracker expects a fresh list each time but internally modifies it, passing a pre-existing list (relationships) could cause unintended side effects.
        # For example, if Tracker modifies self.relationships by appending or removing elements, then the original list (relationships) in your script gets modified as well—leading to unexpected behavior.

     
        self.patterns = {}
        r_types = relations.copy()
        relations = relations
        self.max_depth = max_depth
        depth = 1
        while depth < self.max_depth :
            new_patterns = []
            for rp in relations:
                if len(rp) == depth:
                    for r in r_types:
                        new_patterns.append(rp + r)
            relations.extend(new_patterns)
            depth += 1
            
     
       
        self.patterns = {rp: False for rp in relations}

        

    def show_size(self):
        return('number of keys', len(self.patterns.keys()))

    
    def show_missing(self):
        missing_patterns = []
        present = 0
        missing = 0
        for pattern in self.patterns.keys():
            if self.patterns[pattern] == False:
                 missing += 1
                 missing_patterns.append(pattern)
            else:
                present += 1
      
        return missing_patterns
    
    
    
    #probably have to add non repeating nodes in a path
    def detect_pattern(self, graph: nx.MultiGraph):
        nodes = graph.nodes()
        
        def pattern_search(node: int, pattern: str, depth: int):
            if depth == self.max_depth:
                return
            next_nodes = graph.neighbors(node)

            for next_node in next_nodes:
             
                next_node_data = graph.get_edge_data(node, next_node)

                for i in next_node_data:
                    type_string = (next_node_data[i]['type'])
                    
                    for c in type_string:
                
                        new_pattern = pattern + c
                        self.patterns[new_pattern] = True
                        pattern_search(next_node, new_pattern, depth + 1)
        for node in nodes:
            pattern_search(node, '', 0)
    
