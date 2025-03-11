# The use of this class is detect if there is a pattern present in the graph
# This tracker does not care whether or not access is granted or not, it only 
# cares if the pattern is present

import networkx as nx
from typing import List

class Tracker:
    def __init__(self, relations: list, max_depth: int):
        
        # Thank you Chat GPT for helping me with this
        # Why Your Code Breaks
        # If Tracker expects a fresh list each time but internally modifies it, passing a pre-existing list (relationships) could cause unintended side effects.
        # For example, if Tracker modifies self.relationships by appending or removing elements, then the original list (relationships) in your script gets modified as well—leading to unexpected behavior.

        # Used to track the patterns present in a graph
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
    
    
    

    def detect_pattern(self, graph: nx.MultiGraph):
        nodes = graph.nodes()
        
        def pattern_search(node: int, pattern: str, depth: int, path: List[int]):
            if depth == self.max_depth:
                return

            for next_node in graph.neighbors(node):
                if next_node in path:
                    continue
                
                next_node_data = graph.get_edge_data(node, next_node)
                if next_node_data:
                    for edge_attrs in next_node_data.values():
                        type_string = edge_attrs.get('type', '')
                        
                        for c in type_string:
                            new_pattern = pattern + c
                            self.patterns[new_pattern] = True
                            pattern_search(next_node, new_pattern, depth + 1, path + [next_node])
        for node in nodes:
            pattern_search(node, '', 0, [node])
    
