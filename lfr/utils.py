import json
from networkx import nx
from pymint.mintdevice import MINTDevice
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


def serialize_netlist(device: MINTDevice) -> None:
    # Generate the MINT file from the pyparchmint device
    json_data = device.to_parchmint_v1()
    json_string = json.dumps(json_data)
    json_file = open(get_ouput_path(device.name + ".json"), "wt")
    json_file.write(json_string)
    json_file.close()


def print_netlist(device: MINTDevice) -> None:
    # Generate the MINT file from the pyparchmint device
    minttext = device.toMINT()
    mint_file = open(get_ouput_path(device.name + ".mint"), "wt")
    mint_file.write(minttext)
    mint_file.close()
