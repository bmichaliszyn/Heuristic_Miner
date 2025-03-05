import networkx as nx

# def remove_contents(contents: list, b_list: list) :#-> list:
#     for bucket in b_list:
#         items_to_remove = [item for item in bucket[1] if tuple([item[0], item[-1]]) in contents]
#         for item in items_to_remove:
#             bucket[1].remove(item)
#     return b_list



def find_policy(graph: nx.Graph, n: int, lla: dict, r_types: list):
    
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
    
    
    policy = {rp: None for rp in r_types}
    buckets = {rp: [] for rp in r_types}
   
    nodes = graph.nodes()
    def scout_node(graph: nx.Graph, node: int, lla: dict, depth: int, cur_pattern: str, node_path: list):
        
        if node_path is None:
            node_path = [node]
    
        # Base case
        if depth == 0:
            return
        
        # Grab all next nodes
        next_nodes = graph.neighbors(node)
        
        # For each next node, we will grab the edges' data
        for next_node in next_nodes:
            next_node_data = graph.get_edge_data(node, next_node)
            
            # For each edge, we will grab the type
            for i in next_node_data:
                # Grab the type of each edge
                type_string = next_node_data[i]['type']
                for c in type_string:
                    if next_node not in node_path:
                        new_path = node_path + [next_node]
                        new_pattern = cur_pattern + c
                        
                        # Add every path to the pattern bucket

                        print(f"Appending to buckets[{new_pattern}]: {new_path}")
                        print(new_path[0], new_path[-1])
                        buckets[new_pattern].append(new_path)
                        scout_node(graph, next_node, lla, depth - 1, new_pattern, new_path)
                    else:
                        continue

    
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
    
    def brute_force_check():
     
        # Any bucket containing 0 instances of a pattern is False
        to_be_removed = []
        for b in buckets:
            if b == 'abc':
                print(f"this is {b}, length is {len(buckets[b])}")
            if len(buckets[b]) == 0:
                policy[b] = False
                to_be_removed.append(b)
        for b in to_be_removed:
            del buckets[b]
 
        bucket_list = sorted(buckets.items(), key = lambda item: len(item[1]))
        print('bucket_list', bucket_list)
        
        for i in range(len(bucket_list)):
            cur = bucket_list[i]
            
            grant = 0
            deny = 0
            # Iterate through the paths
            for np in cur[1]:
                start = np[0]
                end = np[-1]
                
                # Based on the LLA, we will add to g or d
                res = (lla[start][end])
                if res == True:
                    grant += 1
                else:
                    deny += 1
                # Exit the current iteration (np) if deny and grant are indicated by the given paths and LLA
                if deny != 0 and grant != 0:
                    break         
                
            if grant > 0 and deny > 0:
                policy[cur[0]] = False
            elif grant > 0:
                policy[cur[0]] = True
            else:
                policy[cur[0]] = False
               
     
    for node in nodes:
        scout_node(graph, node, lla, n , '', [node])
    
    # tbd = []
    # for b in buckets:
    #     if len(buckets[b]) == 0:
    #         tbd.append(b)

    # for b in tbd:
    #     del buckets[b]
        
    # for b in buckets:
    #     print(b, buckets[b])
            
    brute_force_check()
    rules = policy.keys()
    significant_rules = [x for x in rules if policy[x] == True]
    return ('The significant rules are:', significant_rules)