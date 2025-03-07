import pulp
import ant_colony.networkx_ant_colony as ac

def minimum_weight_dominating_set(graph, weights):
    """
    Finds a minimum weight dominating set for a graph.
    
    Parameters:
    graph (nx.Graph): An undirected graph.
    weights (dict): A dictionary with nodes as keys and weights as values.

    Returns:
    list: A list of nodes in the minimum weight dominating set.
    """
    # Create an ILP problem
    prob = pulp.LpProblem("MinimumWeightDominatingSet", pulp.LpMinimize)
    
    # Define binary variables for each node
    x = {i: pulp.LpVariable(f"x_{i}", cat="Binary") for i in graph.nodes()}
    
    # Set the objective to minimize the total weight of the selected nodes
    prob += pulp.lpSum(weights[i] * x[i] for i in graph.nodes())
    
    # Add constraints to ensure each node is dominated
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        prob += x[node] + pulp.lpSum(x[neighbor] for neighbor in neighbors) >= 1
    
    # Solve the ILP problem
    prob.solve()
    
    # Extract the minimum weight dominating set
    dominating_set = [i for i in graph.nodes() if x[i].value() == 1]
    total_weight = sum(weights[node] for node in dominating_set)
    return (dominating_set, total_weight)

