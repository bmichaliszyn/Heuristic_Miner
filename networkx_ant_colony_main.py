import networkx_ant_colony as ac
import copy 
import matplotlib.pyplot as plt
import blank_space as bls


#ToDo:
# Update the initial pheromones with the greedy solution

def main():
        g = ac.generate_connected_erdos_renyi(20, 0.2)
        g1 = copy.deepcopy(g)
        # g2 = copy.deepcopy(g)
        g3 = copy.deepcopy(g)
        
        weights = {node: data['weight'] for node, data in g1.nodes(data = True)}
        
        
        print('Optimal', bls.minimum_weight_dominating_set(g1, weights))
        # print('Greedy', ac.greedy(g2))
        print('Ant-Colony', ac.aco_mcv(g3))
main()        
