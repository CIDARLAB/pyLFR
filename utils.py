from networkx import nx
import parameters
import os


def printgraph(G, filename: str) -> None:
    tt = os.path.join(parameters.OUTPUT_DIR, filename)
    print("output:", parameters.OUTPUT_DIR)
    print("output:", tt)
    nx.nx_agraph.to_agraph(G).write(tt)
