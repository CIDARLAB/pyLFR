import json
import os
from pathlib import Path
from typing import List

import networkx as nx
from pymint.mintdevice import MINTDevice

from lfr.parameters import OUTPUT_DIR


def printgraph(graph: nx.Graph, filename: str, output_dir: Path = OUTPUT_DIR) -> None:
    """Prints the graph in a .dot file and a .pdf file

    Args:
        graph (nx.Graph): graph we need to print
        filename (str): name of the file
        output_dir (Path, optional): Output folder path. Defaults to OUTPUT_DIR.
    """
    # Generate labels and whatnot for the graph
    graph_copy = graph.copy(as_view=False)
    # Print out the dot file and then run the conversion
    dot_path = Path.joinpath(output_dir, f"{filename}.dot")
    pdf_path = Path.joinpath(output_dir, f"{filename}.pdf")
    print("output:", output_dir)
    print("output:", dot_path)
    nx.nx_agraph.to_agraph(graph_copy).write(dot_path)

    os.system(f"dot -Tpdf {str(dot_path.absolute())} -o {str(pdf_path.absolute())}")


def get_ouput_path(filename: str) -> str:
    """Returns the path to the output file"""
    return os.path.join(OUTPUT_DIR, filename)


def serialize_netlist(output_path: Path, mint_device: MINTDevice) -> None:
    """Serializes the netlist to a json file"""

    # Generate the MINT file from the pyparchmint device
    json_data = mint_device.to_parchmint()
    json_string = json.dumps(json_data)
    file_path = output_path.joinpath(f"{mint_device.device.name}.json")
    json_file = open(file_path, "wt")
    json_file.write(json_string)
    json_file.close()


def print_netlist(output_path: Path, mint_device: MINTDevice) -> None:
    """Prints the netlist to the console"""

    # Generate the MINT file from the pyparchmint device
    minttext = mint_device.to_MINT()
    file_path = Path.joinpath(output_path, f"{mint_device.device.name}.mint")
    mint_file = open(file_path, "wt")
    mint_file.write(minttext)
    mint_file.close()


def convert_list_to_str(lst: List) -> str:
    """Returns a string list formatted as a string

    Args:
        lst (List): list we need to convert into a string

    Returns:
        str: list formatted as a string
    """
    ret = "[{0}]".format(", ".join([str(i) for i in lst]))
    return ret
