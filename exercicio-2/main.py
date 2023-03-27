import matplotlib.pyplot as plt
import networkx


if __name__ == "__main__":
    graph = networkx.erdos_renyi_graph(n=12, p=0.16)
    print(networkx.average_clustering(graph))
    print(len(graph.edges))
