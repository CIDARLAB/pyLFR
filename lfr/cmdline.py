import argparse
import glob
import json
import os

from art import tprint

import lfr.parameters as parameters
from lfr.api import compile_lfr
from lfr.netlistgenerator.mappinglibrary import MappingLibrary


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
    # Print LFR ASCII Banner
    tprint("---- LFR ----")
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
    parser.add_argument(
        "--pre-load",
        type=str,
        action="append",
        help=(
            "This lets the preprocessor look for the different design libraries that"
            " need to be added to the memory (avoid using this outside bulk testing)"
        ),
    )
    args = parser.parse_args()

    # Generate proxy variables for the parsed args
    input_files = args.input
    outpath = args.outpath
    technology = args.technology
    library_path = args.library
    no_mapping_flag = args.no_mapping
    no_gen_flag = args.no_gen
    no_annotations_flag = args.no_annotations
    pre_load = args.pre_load

    compile_lfr(
        input_files=input_files,
        outpath=outpath,
        technology=technology,
        library_path=library_path,
        no_mapping_flag=no_mapping_flag,
        no_gen_flag=no_gen_flag,
        no_annotations_flag=no_annotations_flag,
        pre_load=pre_load,
    )


if __name__ == "__main__":
    main()
