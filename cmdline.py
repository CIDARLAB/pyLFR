import os
from pathlib import Path
from antlr4 import ParseTreeWalker, CommonTokenStream, FileStream
from antlr.lfrXLexer import lfrXLexer
from antlr.lfrXParser import lfrXParser
from mappingCompiler import MappingCompiler
from netlistgenerator.devicegenerator import DeviceGenerator
from netlistgenerator.mappinglibrary import MappingLibrary
import argparse
import parameters
import glob
import json

def load_libraries():
    library = dict()
    os.chdir(parameters.LFR_DIR)
    for filename in glob.glob("*.json"):
        file = open(filename, 'r')
        lib_object = json.loads(file.read())
        library[lib_object['name']] = MappingLibrary(lib_object)
    return library


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input', help="This is the file thats used as the input ")
    parser.add_argument('--outpath', type=str, default="out/", help="This is the output directory")
    parser.add_argument('--library', type=str, default="dropx", help="This is the mapping library you need to use")

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

    library_name = args.library
    libraries = load_libraries()
    if library_name not in libraries.keys():
        raise Exception("Could not find mapping library")
    
    library = libraries[library_name]
    
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
        devicegenerator = DeviceGenerator(mapping_listener.currentModule.name, mapping_listener.currentModule, library)
        devicegenerator.generate_fluidic_netlist()
        devicegenerator.size_netlist()

        devicegenerator.print_netlist()
        


if __name__ == "__main__":
    main()
