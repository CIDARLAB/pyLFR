import argparse
import glob
import json
import os
import sys
from pathlib import Path

from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker

import lfr.parameters as parameters
from lfr.antlrgen.lfrXLexer import lfrXLexer
from lfr.antlrgen.lfrXParser import lfrXParser
from lfr.moduleinstanceListener import ModuleInstanceListener
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.netlistgenerator.v2.generator import (
    generate,
    generate_dropx_library,
    generate_mars_library,
)
from lfr.postProcessListener import PostProcessListener
from lfr.preprocessor import PreProcessor
from lfr.utils import print_netlist, printgraph, serialize_netlist


def load_libraries():
    library = {}
    os.chdir(parameters.LIB_DIR)
    print(" LIB Path : " + str(parameters.LIB_DIR))
    for filename in glob.glob("*.json"):
        file = open(filename, "r")
        lib_object = json.loads(file.read())
        library[lib_object["name"]] = MappingLibrary(lib_object)
    return library


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input", nargs="+", help="This is the file thats used as the input "
    )
    parser.add_argument(
        "--outpath", type=str, default="out/", help="This is the output directory"
    )
    parser.add_argument(
        "--technology",
        type=str,
        # default="dropx",
        default="mars",
        help="This is the mapping library you need to use",
    )
    parser.add_argument(
        "--library",
        type=str,
        default="./library",
        help="This sets the default library where the different technologies sit in",
    )
    parser.add_argument("--no-mapping", help="Skipping Explicit Mappings")
    parser.add_argument(
        "--no-gen",
        action="store_true",
        help="Force the program to skip the device generation",
    )
    parser.add_argument(
        "--no-annotations",
        action="store_true",
        help=(
            "Force the compiler to skip reading postprocess annotations like #MAP and"
            " #CONSTRAIN"
        ),
    )
    args = parser.parse_args()

    # Utilize the prepreocessor to generate the input file
    preprocessor = PreProcessor(args.input)

    if preprocessor.check_syntax_errors():
        print("Stopping compiler because of syntax errors")
        sys.exit(0)

    preprocessor.process()

    print("output dir:", args.outpath)
    print(args.input)

    rel_input_path = "pre_processor_dump.lfr"
    input_path = Path(rel_input_path).resolve()

    abspath = os.path.abspath(args.outpath)
    parameters.OUTPUT_DIR = abspath

    if os.path.isdir(abspath) is not True:
        print("Creating the output directory:")
        path = Path(parameters.OUTPUT_DIR)
        path.mkdir(parents=True)

    library_name = args.technology
    # libraries = load_libraries()
    # if library_name not in libraries.keys():
    #     raise Exception("Could not find mapping library")

    library = None
    # library = libraries[library_name]

    # Modifiy this to translate relative path to absolute path in the future
    finput = FileStream(str(input_path))

    lexer = lfrXLexer(finput)

    stream = CommonTokenStream(lexer)

    parser = lfrXParser(stream)

    tree = parser.skeleton()

    walker = ParseTreeWalker()

    if args.no_annotations is True:
        mapping_listener = ModuleInstanceListener()
    else:
        mapping_listener = PostProcessListener()

    walker.walk(mapping_listener, tree)

    mapping_listener.print_stack()

    mapping_listener.print_variables()

    interactiongraph = mapping_listener.currentModule.FIG

    printgraph(interactiongraph, mapping_listener.currentModule.name + ".dot")

    if args.no_gen is True:
        sys.exit(0)

    # Check if the module compilation was successful
    if mapping_listener.success:
        # Now Process the Modules Generated
        # V2 generator
        if args.technology == "dropx":
            library = generate_dropx_library()
        elif args.technology == "mars":
            library = generate_mars_library()
        elif args.technology == "mlsi":
            print("Implement Library for MLSI")
            pass
        else:
            print("Implement Library for whatever else")
            pass

        if mapping_listener.currentModule is None:
            raise ValueError()
        if library is None:
            raise ValueError()
        unsized_device = generate(mapping_listener.currentModule, library)

        print_netlist(unsized_device)
        serialize_netlist(unsized_device)


if __name__ == "__main__":
    main()
