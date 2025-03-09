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
    for key in policy.keys():
        if policy[key] is None:
            return False
    return True

def examine(node: int, graph: nx.Graph, neighbors: set, lla: dict, policy: dict, n: int, cd: set, cg :set):
    grant_dict = {}
 
    targets = [neighbor for neighbor in neighbors if lla[node][neighbor] is True]
  
    grants, denies = find_viable_paths(graph, node, targets, n) 
    
    # If we find a new deny we must update our policy, checking a set will be faster (not sure)
  
    for d in denies:
        if d not in cd:
            cd.add(d)
            policy[d] = False
            
    for g in grants:
        target_node, path = g[0], g[1]
        if path in cd:
            continue      
        grant_dict.setdefault((node, target_node), []).append(path)
    
    check_existing_grants = False
    add_to_npg = []
    
    for key, paths in grant_dict.items():
      
        if len(paths) == 1 and paths[0] not in cg:
            cg.add(paths[0])
            policy[paths[0]] = True
            check_existing_grants = True
        else:
            add_to_npg.extend(((node, key), path) for path in paths)
            
    return check_existing_grants, add_to_npg
   
def find_viable_paths(graph: nx.Graph, node: int, targets:List[int], max_length: int):
    g_paths, d_paths= [], [] #cur node, cur path for g_paths
    
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
                            g_paths.append((next_node, new_path))
                        else:
                            d_paths.append(new_path)
                        seek(next_node, depth + 1, new_path, new_visited)
                        
    seek(node, 0, '', {node})

    return g_paths, d_paths

def grant_check(policy: dict, cg: set, npg: dict, cd: set):
    ('performing')
    # Create a list of keys to delete after iteration
    to_delete = []

    for np in list(npg.keys()):  # Iterate over a copy to modify safely
        # Remove grants that are in 'cd'
        npg[np] = [grant for grant in npg[np] if grant not in cd]

        if len(npg[np]) == 1:  # If only one grant remains
            grant = npg[np][0]  # Extract the single grant
            cg.add(grant)  # Add to confirmed grants
            policy[grant] = True  # Mark as approved

        if not npg[np]:  # If no grants remain, mark for deletion
            to_delete.append(np)

    # Remove node pairs with no grants left
    for np in to_delete:
        del npg[np]

def hueristic_miner(lla: dict, depth: int, r_types: List[str], graph: nx.Graph, max_iterations: int):
    #####
    start = time.time()
    #####
    confirmed_denies, confirmed_grants = set(), set()
    policy = create_policy(depth, r_types)
    node_pair_grants = {}
    nodes_checked = 0
    iterations = 0
    checked_nodes= []

    node_list = [(node, *find_connectivity(node, depth, graph)) for node in graph.nodes()]

    sorted_node_list = sorted(node_list, key=lambda x: x[1])

    sorted_node_list = [n for n in sorted_node_list if n[1] > 0]  # Remove non-connected nodes

    while not complete_policy(policy) and iterations < max_iterations:
        
        for node, _, neighbors in sorted_node_list:    
            print(node)
            if complete_policy(policy):
                break    
            check_existing_grants, add_to_npg = examine(node, graph, neighbors, lla, policy, depth, confirmed_denies, confirmed_grants)
            if check_existing_grants:
                grant_check(policy, confirmed_grants, node_pair_grants, confirmed_denies)
            for npg in add_to_npg:
                node_pair_grants.setdefault(npg[0], []).append(npg[1])
            nodes_checked += 1
            checked_nodes.append(node)
            
        iterations +=1
    end = time.time()
    elapsed_time = end - start
    denies = sum(1 for p in policy if policy[p] is False)
    grants = sum(1 for p in policy if policy[p] is True)
    ambiguous = sum(1 for p in policy if policy[p] is None)
    print(f'Iterations: {iterations}, Nodes checked: {nodes_checked}, Denies: {denies}, Grants: {grants}, Ambiguous: {ambiguous}')
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Nodes checked were: {checked_nodes}")
    for rule in policy.keys():
        if policy[rule] == True:
            print (rule)
    return policy
