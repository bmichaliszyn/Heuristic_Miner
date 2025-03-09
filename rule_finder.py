# The weakness of this algorithm is you may run across false positives.
# For example, if "a,a,a" is a rule, but "a,a,b" shares a path with a node 
# pair that contains "a,a,a" the algo may not determine that "a,a,b" is false
# another node pair must have "a,a,b" and deny access to determine that "a,a,a"
# is granting access and NOT "a,a,b"

import networkx as nx
from typing import List
import time

def find_policy(graph: nx.Graph, n: int, lla: dict, r_types: List[str]):
    start = time.time()
    
    # This allows us to create buckets for each relationship pattern (contians node pairs)
    # along with a policy that contains all relationship patterns (all set true)
    policy = {}
        
    depth = 1
    while depth < n:
        new_patterns = []
        for rp in r_types:
            if len(rp) == depth:
                for r in r_types:
                    new_pattern = rp + r
                    if len(new_pattern) <= n:
                        new_patterns.append(new_pattern)
        r_types.extend(new_patterns)
        depth += 1
    
    
    policy = {rp: True for rp in r_types}
    buckets = {rp: [] for rp in r_types}
   
    nodes = graph.nodes()
    def scout_node(graph: nx.Graph, node: int, depth: int, cur_pattern: str, node_path: list):

        if depth == 0:
            return
        
        # Grab all next nodes
        next_nodes = graph.neighbors(node)
        
        # For each next node, we will grab the edges' data
        for next_node in next_nodes:
            next_node_data = graph.get_edge_data(node, next_node)
            
            # For each edge, we will grab the type
            for edge_attrs in next_node_data.values():
                # Grab the type of each edge
                type_string = edge_attrs.get('type', '')
                for c in type_string:
                    if next_node not in node_path:  
                        
                        # Add every path to the pattern bucket
                        buckets[cur_pattern + c].append(node_path + [next_node])
                        scout_node(graph, next_node, depth - 1, cur_pattern + c, node_path + [next_node])
                    else:
                        continue

    def brute_force_check():
        # Any bucket containing 0 instances of a pattern is False
        to_be_removed = []
        for b in buckets:
            if len(buckets[b]) == 0:
                policy[b] = False
                to_be_removed.append(b)
        for b in to_be_removed:
            del buckets[b]
 
        bucket_list = sorted(buckets.items(), key = lambda item: len(item[1]))
       
        for i in range(len(bucket_list)):
            cur = bucket_list[i]
            
            # Iterate through the paths cur[0] is the pattern 'ac', and cur[1] are the paths [1,2,3], [2,1,4]
            for np in cur[1]:
    
                start = np[0]
                end = np[-1]
                
                if lla[start][end] == False:                    
                    policy[cur[0]] = False
            
    # Find the node paths with max length n 
    for node in nodes:
        scout_node(graph, node, n , '', [node])
    
    brute_force_check()
    end = time.time()
    elapsed_time = end - start
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    rules = policy.keys()
    significant_rules = [x for x in rules if policy[x] == True]
    
    # prints out each bucket and the node paths if the rule remains true
    # for rule in significant_rules:
    #     print(rule, buckets[rule])
        
    # Return the correct result with proper spelling and grammar     
    if len(significant_rules) == 1:
        return f"The significant rule is:\n{significant_rules}\nThere is {len(significant_rules)} significant rules"
    else:
        return f"The significant rules are:\n{significant_rules}\nThere are {len(significant_rules)} significant rules"

    
    # def policy_check():
    #     to_be_removed = []
    #     for b in buckets:
    #         # Any bucket containing 0 instances of a pattern is False
    #         if len(buckets[b]) == 0:
    #             policy[b] = False
    #             to_be_removed.append(b)
    #     for b in to_be_removed:
    #         del buckets[b]
    #     # Sort the buckets by amount of nodes contained in the path
    
    
    #     bucket_list = sorted(buckets.items(), key = lambda item: len(item[1]))
        
        
    #     while bucket_list:
    #         cur = bucket_list.pop(0)
    #         grant = 0
    #         deny = 0
    #         for np in cur[1]:
    #             start = np[0]
    #             end = np[len(np)-1]
    #             res = (lla[start][end])
    #             if res == True:
    #                 grant +=1
    #             else:
    #                 deny +=1
    #             if deny != 0 and grant != 0:
    #                 break
    #         if grant > 0 and deny > 0:
    #             bucket_list.append(cur)
    #             continue
    #         contents = [tuple([x[0], x[-1]]) for x in cur]
    #         if grant > 0:
    #             policy[cur[0]] = True
    #             bucket_list = remove_contents(contents, bucket_list)
    #         else:
    #             policy[cur[0]] = False
    #             bucket_list = remove_contents(contents, bucket_list)
    #         bucket_list = bucket_list[:1]
    