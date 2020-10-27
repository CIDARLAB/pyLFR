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
from lfr.netlistgenerator.v2.generator import generate_dropx_library, generate
from lfr.utils import print_netlist, printgraph, serialize_netlist


def load_libraries():
    library = dict()
    os.chdir(parameters.LIB_DIR)
    print(" LIB Path : " + str(parameters.LIB_DIR))
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
    parser.add_argument('--no-mapping', help="Skipping Explicit Mappings")
    parser.add_argument('--no-gen', help="Force the program to skip the device generation")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    print("Input Path: {0}".format(input_path))

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
    # libraries = load_libraries()
    # if library_name not in libraries.keys():
    #     raise Exception("Could not find mapping library")

    library = None
    # library = libraries[library_name]

    # Modifiy this to translate relative path to absolute path in the future
    finput = FileStream(input_path)

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

        # V2 generator
        library = generate_dropx_library()

        unsized_device = generate(mapping_listener.currentModule, library)

        unsized_device.toMINT()

        printgraph(mapping_listener.currentModule.FIG, mapping_listener.currentModule.name)
        print_netlist(unsized_device)
        serialize_netlist(unsized_device)


if __name__ == "__main__":
    main()
