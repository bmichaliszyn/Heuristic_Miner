import networkx_ant_colony as ac
import random 
import networkx as nx
import matplotlib.pyplot as plt

def main():
        g = ac.generate_connected_erdos_renyi(100, 0.04)

        for n in g.nodes:
                g.nodes[n]['weight'] = random.randint(10,20)
                g.nodes[n]['pheromone'] = 1
                g.nodes[n]['selected'] = False
        


        print(g)
        print(ac.aco_mcv(g))
        nx.draw(g)
        plt.show()

main()        
