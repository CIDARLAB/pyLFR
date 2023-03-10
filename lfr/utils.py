import json
import os
from typing import List

import networkx as nx
from pymint.mintdevice import MINTDevice
from pathlib import Path

from lfr.parameters import OUTPUT_DIR


def printgraph(G: nx.Graph, filename: str, output_dir: Path=OUTPUT_DIR) -> None:
    """Prints the graph in a .dot file and a .pdf file"""

    # Generate labels and whatnot for the graph
    H = G.copy(as_view=False)
    # Print out the dot file and then run the conversion
    tt = os.path.join(output_dir, filename)
    print("output:", output_dir)
    print("output:", tt)
    nx.nx_agraph.to_agraph(H).write(tt)

    os.system("dot -Tpdf {} -o {}.pdf".format(tt, tt))


def get_ouput_path(filename: str) -> str:
    """Returns the path to the output file"""
    return os.path.join(OUTPUT_DIR, filename)


def serialize_netlist(mint_device: MINTDevice) -> None:
    """Serializes the netlist to a json file"""

    # Generate the MINT file from the pyparchmint device
    json_data = mint_device.to_parchmint()
    json_string = json.dumps(json_data)
    json_file = open(get_ouput_path(mint_device.device.name + ".json"), "wt")
    json_file.write(json_string)
    json_file.close()


def print_netlist(mint_device: MINTDevice) -> None:
    """Prints the netlist to the console"""

    # Generate the MINT file from the pyparchmint device
    minttext = mint_device.to_MINT()
    mint_file = open(get_ouput_path(mint_device.device.name + ".mint"), "wt")
    mint_file.write(minttext)
    mint_file.close()


def convert_list_to_str(lst: List) -> str:
    """Returns a string list formatted as a string

    Args:
        lst (List): list we need to convert into a string

    Returns:
        str: list formatted as a string
    """
    ret = "[{}]".format(", ".join([str(i) for i in lst]))
    return ret
