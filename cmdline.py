import sys
import os
from pathlib import Path

from antlr4 import *
from antlr.lfrXLexer import lfrXLexer
from antlr.lfrXParser import lfrXParser
from lfrCompiler import LFRCompiler
from mappingCompiler import MappingCompiler
from netlistgenerator.devicegenerator import DeviceGenerator

import argparse
import parameters


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'input', help="This is the file thats used as the input ")
    parser.add_argument('--outpath', type=str, default="out/",
                        help="This is the output directory")

    args = parser.parse_args()
    print("output dir:", args.outpath)
    print(args.input)

    extension = Path(args.input).suffix
    if extension != '.lfr' :
        print("Unrecognized file Extension")
        exit()

    abspath = os.path.abspath(args.outpath)
    parameters.OUTPUT_DIR = abspath

    if os.path.isdir(abspath) is not True:
        print("Creating the output directory:")
        path = Path(parameters.OUTPUT_DIR)
        path.mkdir(parents=True)

    finput = FileStream(args.input)

    lexer = lfrXLexer(finput)

    stream = CommonTokenStream(lexer)

    parser = lfrXParser(stream)

    tree = parser.skeleton()

    walker = ParseTreeWalker()

    # listener = LFRCompiler()

    # walker.walk(listener, tree)

    mapping_listener = MappingCompiler()

    walker.walk(mapping_listener, tree)

    # Check if the module compilation was successful
    if mapping_listener.success:
        # Now Process the Modules Generated
        devicegenerator = DeviceGenerator(
            mapping_listener.currentModule.name, mapping_listener.currentModule)
        devicegenerator.generate_netlist()


if __name__ == "__main__":
    main()
