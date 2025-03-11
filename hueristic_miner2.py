import networkx as nx 
from typing import List
from collections import deque
import time
def create_policy(n: int, r_types: List[str]) -> dict:
    depth = 1
    patterns = set(r_types)

    while depth < n:
        new_patterns = set()
        for rp in patterns:
            for r in r_types:
                new_pattern = rp + r
                if len(new_pattern) <= n:
                    new_patterns.add(new_pattern)
        patterns.update(new_patterns)
        depth += 1
    policy = {rp: None for rp in patterns}
    return policy
                 
def find_connectivity(node: int, depth: int, graph: nx.Graph) -> int:
    visited = set()
    queue = deque([(node, 0)])
    connectivity = 0
    
    while queue:
        cur_node, distance = queue.popleft()
        if distance > depth:
            continue
      
        visited.add(cur_node)
        connectivity +=1
        
        for neighbor in graph.neighbors(cur_node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    # Remove self from neighbors
    visited.remove(node)
    return connectivity-1, visited

def complete_policy(policy:dict):
    return all(value is not None for value in policy.values())

def examine(node: int, graph: nx.Graph, neighbors: set, lla: dict, policy: dict, n: int, cd: set, cg :set, proof: set, r_pairs: set):
    grant_dict = {}
    targets = [neighbor for neighbor in neighbors if lla.get(node, {}).get(neighbor) is True]
    grants, denies = find_viable_paths(graph, node, targets, n) 
    check_existing_grants = False
    add_to_npg = []
    
    # If we find a new deny we must update our policy, checking a set will be faster (not sure)
    # In addition, anytime we find something out about the policy, we must look at the unsolved node pairs
  
    for d in denies:
        pattern, visited, target_node = d[0], d[1], d[2]
        if pattern not in cd:
            
            cd.add(pattern)
            policy[pattern] = False
            check_existing_grants = True
            proof |= visited
            r_pairs.add((node, target_node))
            
            
    # Each potential grant path is filtered out by confirmed denies. 
    # The remaining ones are added to a dictionary with key as a tuple (source, target), value is a tuple (path, visited)
    for g in grants:                                                                    
        target_node, path, visited = g[0], g[1], g[2]
        if path in cd:
            continue      
        grant_dict.setdefault((node, target_node), []).append((path, visited))
        
        # This line is actually so huge. Even if one iteration doesn't use an 
        proof |= visited
    
    for key, paths in grant_dict.items():
        if len(paths) == 1:
            path, visited = paths[0]  
            if path not in cg:
                cg.add(path)
                policy[path] = True
                proof |= visited  
                r_pairs.add((node, key[1]))
        else:
            add_to_npg.extend((key, p_v) for p_v in paths)
            
    return check_existing_grants, add_to_npg
   
def find_viable_paths(graph: nx.Graph, node: int, targets:List[int], max_length: int):
    g_paths, d_paths= [], [] #next_node, new_path, new_visited for g_paths | new,path, new_visited, for d_paths
    
    def seek(node: int, depth: int, path: str, visited: set):
        #Base Case
        if depth >= max_length:
            return
        # Grab all neighbors
        for next_node in graph.neighbors(node):
            if next_node not in visited:
                new_visited = visited | {next_node}
                # Grab all edge types
                next_node_data = graph.get_edge_data(node,next_node)
                
                for edge_attrs in next_node_data.values():
                    type_string = edge_attrs.get('type', '')
                    # Iterate through all the types
                    for c in type_string:
                        new_path = path + c
                        # If the original node is granted access we add to the g_path else, to the d_paths
                        if next_node in targets:
                            g_paths.append((next_node, new_path, new_visited))
                        else :                                                     ############NEED LLA SEARCH HERE
                            d_paths.append((new_path, new_visited, next_node))
                        seek(next_node, depth + 1, new_path, new_visited)
                        
    seek(node, 0, '', {node})

    return g_paths, d_paths

def grant_check(policy: dict, cg: set, npg: dict, cd: set, proof: set, r_pairs: set): # need to add proof here as well
    # Create a list of keys to delete after iteration
    to_delete = []

    for np in list(npg.keys()):  # Iterate over a copy to modify safely
         # (source, target), (pattern, visited)
        # Remove grants_paths that are in 'cd'
        npg[np] = [grant_path for grant_path in npg[np] if grant_path[0] not in cd] ###

        # If only one grant remains, we can add it to confirmed grants
        if len(npg[np]) == 1:  
            grant = npg[np][0][0]
            visited = npg[np][0][1]
            cg.add(grant)  
            policy[grant] = True  
            proof |= visited
            r_pairs.add((np[0], np[1]))
            to_delete.append(np)
            
        
        # If every grant path has been proven correct, the node is not worth iterating over 
        elif all(grant_path[0] in cg for grant_path in npg[np]):
                to_delete.append(np)

    # Remove node pairs with no grants left
    for np in to_delete:
        r_pairs.discard((np[0], np[1]))
        del npg[np]
        
def count_bools_2d_dict(data: dict) -> int:
    return sum(
        isinstance(value, bool) 
        for sub_dict in data.values() 
        for value in sub_dict.values()
    )

def hueristic_miner(lla: dict, depth: int, r_types: List[str], graph: nx.Graph, max_iterations: int):
    #####
    start = time.time()
    #####
    confirmed_denies, confirmed_grants = set(), set()
    policy = create_policy(depth, r_types)
    node_pair_grants = {}
    nodes_checked = 0
    iterations = 0
    checked_nodes= set()
    proof = set()
    relevant_pairs = set()

    # Pre-process all nodes to find their connectivity. Sort them by lowest first and remove all nodes containing 0 connections.
    node_list = [(node, *find_connectivity(node, depth, graph)) for node in graph.nodes()]
    sorted_node_list = sorted(node_list, key=lambda x: x[1])
    # sorted_node_list = [n for n in sorted_node_list if n[1] > 0]  # Remove non-connected nodes

    # Flag function will stop iterations if we complete the policy
    while not complete_policy(policy) and iterations < max_iterations:
        for node, _, neighbors in sorted_node_list:    
            if complete_policy(policy):
                break    
            
            # If we find new denies, we must check the existing node-pair grants to see if we can determine a True grant.
            # Each time we examine a node, any node-pair grants that were discovered but not confirmed to be True will be stored
            check_existing_grants, add_to_npg = examine(node, graph, neighbors, lla, policy, depth, confirmed_denies, confirmed_grants, proof, relevant_pairs)
            if check_existing_grants and len(node_pair_grants) > 0:
                grant_check(policy, confirmed_grants, node_pair_grants, confirmed_denies, proof, relevant_pairs)
                
            # Add the new node pair grants
            for npg in add_to_npg:
                node_pair_grants.setdefault(npg[0], []).append(npg[1])
            
            nodes_checked += 1
            checked_nodes.add(node)
            
        iterations +=1
    end = time.time()
    elapsed_time = end - start
    denies = sum(1 for p in policy if policy[p] is False)
    grants = sum(1 for p in policy if policy[p] is True)
    ambiguous = sum(1 for p in policy if policy[p] is None)
    print(f'Iterations: {iterations}, Nodes checked: {nodes_checked}, Denies: {denies}, Grants: {grants}, Ambiguous: {ambiguous}')
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    
    list_of_grants = []
    for p in policy:
        if policy[p] == True:
            list_of_grants.append(p)
    print(f'The grant policies were discovered to be {list_of_grants}')
    print(f'We involved {len(proof)} nodes in securing the policy')
    print(f'There are {len(relevant_pairs)} relavent pairs')
    rpp = list(proof)
    reduced_lla = {}
    
    # Creating a reduced lla for testing policies
    for i in rpp:
        reduced_lla[i] = {}
        for j in rpp:
            if i in lla and j in lla[i]:
                reduced_lla[i][j] = lla[i][j]

    
    return reduced_lla
