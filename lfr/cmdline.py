from lfr.lfrCompiler import LFRCompiler
import os
from pathlib import Path
from antlr4 import ParseTreeWalker, CommonTokenStream, FileStream
from lfr.antlrgen.lfrXLexer import lfrXLexer
from lfr.antlrgen.lfrXParser import lfrXParser
from lfr.mappingCompiler import MappingCompiler
from lfr.netlistgenerator.devicegenerator import DeviceGenerator
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
import argparse
import lfr.parameters as parameters
import glob
import json
import lfr.utils as utils


def load_libraries():
    library = dict()
    os.chdir(parameters.LIB_DIR)
    print(" LIB Path : " + parameters.LIB_DIR)
    for filename in glob.glob("*.json"):
        file = open(filename, 'r')
        lib_object = json.loads(file.read())
        library[lib_object['name']] = MappingLibrary(lib_object)
    return library


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input', help="This is the file thats used as the input ")
    parser.add_argument('--outpath', type=str, default="out/", help="This is the output directory")
    parser.add_argument('--technology', type=str, default="dropx", help="This is the mapping library you need to use")
    parser.add_argument('--library', type=str, default="./library", help="This sets the default library where the different technologies sit in")
    args = parser.parse_args()
    print("output dir:", args.outpath)
    print(args.input)

    extension = Path(args.input).suffix
    if extension != '.lfr':
        print("Unrecognized file Extension")
        exit()

    abspath = os.path.abspath(args.outpath)
    parameters.OUTPUT_DIR = abspath

    if os.path.isdir(abspath) is not True:
        print("Creating the output directory:")
        path = Path(parameters.OUTPUT_DIR)
        path.mkdir(parents=True)

    # abspath = os.path.abspath(args.library)
    # parameters.LIB_DIR = abspath

    library_name = args.technology
    libraries = load_libraries()
    if library_name not in libraries.keys():
        raise Exception("Could not find mapping library")

    library = libraries[library_name]

    # TODO: Modifiy this to translate relative path to absolute path in the future
    finput = FileStream(args.input)

    lexer = lfrXLexer(finput)

    stream = CommonTokenStream(lexer)

    parser = lfrXParser(stream)

    tree = parser.skeleton()

    walker = ParseTreeWalker()

    mapping_listener = LFRCompiler()

    walker.walk(mapping_listener, tree)

    mapping_listener.print_stack()

    mapping_listener.print_variables()

    interactiongraph = mapping_listener.currentModule.FIG

    utils.printgraph(interactiongraph, mapping_listener.currentModule.name + ".dot")

    # Check if the module compilation was successful
    if mapping_listener.success:
        # Now Process the Modules Generated
        devicegenerator = DeviceGenerator(mapping_listener.currentModule.name, mapping_listener.currentModule, library)
        # devicegenerator.generate_fluidic_netlist()
        # # devicegenerator.size_netlist()

        # devicegenerator.print_netlist()
        # devicegenerator.serialize_netlist()
        pass


if __name__ == "__main__":
    main()
