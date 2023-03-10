import os
import sys
from pathlib import Path
from typing import List

from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker

from lfr import parameters
from lfr.antlrgen.lfr.lfrXLexer import lfrXLexer
from lfr.antlrgen.lfr.lfrXParser import lfrXParser
from lfr.moduleinstanceListener import ModuleInstanceListener
from lfr.netlistgenerator.generator import (
    generate,
    generate_dropx_library,
    generate_mars_library,
    generate_mlsi_library,
)
from lfr.postProcessListener import PostProcessListener
from lfr.preprocessor import PreProcessor
from lfr.utils import print_netlist, printgraph, serialize_netlist


def compile_lfr(
    input_files: List[str],
    outpath: str = "out/",
    technology: str = "dropx",
    library_path: str = "./library",
    no_mapping_flag: bool = False,
    no_gen_flag: bool = False,
    no_annotations_flag: bool = False,
    pre_load: List[str] = [],
) -> int:
    """Standard API to compile a lfr file

    This is the hook that we use for running lfr files from the command line or in
    programs. Assumes that all the paths for the input files exist. It can create
    the output directories if they aren't present.

    Args:
        input_files (List[str]): The paths for the input lfr files
        outpath (str, optional): The path where all the outputs are saved. Defaults to "out/".
        technology (str, optional): String for library that we need to use. Defaults to "dropx".
        library_path (str, optional): path where all the library files are placed. Defaults to "./library".
        no_mapping_flag (bool, optional): Enables/Disables mapping. Defaults to False.
        no_gen_flag (bool, optional): Enables/Disables device generation. Defaults to False.
        no_annotations_flag (bool, optional): Skip Annotation parsing. Defaults to False.
        pre_load (List[str], optional): Preload Directory. Defaults to [].

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        int: 0 if the compilation was successful, >0 if theres an error
    """
    pre_load_file_list = pre_load
    print(pre_load_file_list)
    # Utilize the prepreocessor to generate the input file
    preprocessor = PreProcessor(input_files, pre_load_file_list)

    if preprocessor.check_syntax_errors():
        print("Stopping compiler because of syntax errors")
        return 0

    preprocessor.process()

    print("output dir:", outpath)
    print(input_files)

    rel_input_path = "pre_processor_dump.lfr"
    input_path = Path(rel_input_path).resolve()

    abspath = Path(outpath).absolute()
    parameters.OUTPUT_DIR = abspath

    if os.path.isdir(abspath) is not True:
        print("Creating the output directory:")
        path = Path(parameters.OUTPUT_DIR)
        path.mkdir(parents=True)

    library = None
    # library = libraries[library_name]

    # Modifiy this to translate relative path to absolute path in the future
    finput = FileStream(str(input_path))

    lexer = lfrXLexer(finput)

    stream = CommonTokenStream(lexer)

    parser = lfrXParser(stream)

    tree = parser.skeleton()

    walker = ParseTreeWalker()

    if no_annotations_flag is True:
        mapping_listener = ModuleInstanceListener()
    else:
        mapping_listener = PostProcessListener()

    walker.walk(mapping_listener, tree)

    mapping_listener.print_stack()

    mapping_listener.print_variables()

    if mapping_listener.currentModule is not None:
        interactiongraph = mapping_listener.currentModule.FIG
        printgraph(interactiongraph, mapping_listener.currentModule.name + ".dot")

    if no_gen_flag is True:
        return 0

    # Check if the module compilation was successful
    if mapping_listener.success:
        # Now Process the Modules Generated
        # V2 generator
        if technology == "dropx":
            library = generate_dropx_library()
        elif technology == "mars":
            library = generate_mars_library()
        elif technology == "mlsi":
            library = generate_mlsi_library()
        else:
            print("Implement Library for whatever else")
            pass

        if mapping_listener.currentModule is None:
            raise ValueError()
        if library is None:
            raise ValueError()
        unsized_devices = generate(mapping_listener.currentModule, library)

        for unsized_device in unsized_devices:
            print_netlist(unsized_device)
            serialize_netlist(unsized_device)
