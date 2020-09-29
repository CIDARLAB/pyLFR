from networkx import nx
import lfr.parameters as parameters
import os


def printgraph(G, filename: str) -> None:
    tt = os.path.join(parameters.OUTPUT_DIR, filename)
    print("output:", parameters.OUTPUT_DIR)
    print("output:", tt)
    nx.nx_agraph.to_agraph(G).write(tt)

    os.system('dot -Tpdf {} -o {}.pdf'.format(tt, tt))


def get_ouput_path(filename: str) -> str:
    return os.path.join(parameters.OUTPUT_DIR, filename)