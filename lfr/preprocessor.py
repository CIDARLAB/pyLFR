import re
import sys
from pathlib import Path
from typing import Dict, List

import networkx as nx
from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.FileStream import FileStream

from lfr.antlrgen.lfr.lfrXLexer import lfrXLexer
from lfr.antlrgen.lfr.lfrXParser import lfrXParser

IMPORT_FILE_PATTERN = r"(`import\s+\"(\w+.lfr)\")"


class PreProcessor:
    def __init__(self, file_list: List[str], lib_dir_list: List[str] = []) -> None:
        self.resolved_paths = {}
        self.full_text = {}
        self.text_dump = None
        self._lib_file_list: Dict[str, str] = {}  # Stores file path to file

        print("Loading all LFR Files from lib Directories:")
        for dir_ref in lib_dir_list:
            print("-- Loading form path {}".format(dir_ref))
            path = Path(dir_ref).resolve()

            for file in path.rglob("*.lfr"):
                path_object = Path(file)
                full_path = path_object.resolve()
                print("Storing into library: {}".format(full_path))
                self._lib_file_list[str(path_object.name)] = str(full_path)

        for file_path in file_list:

            extension = Path(file_path).suffix
            if extension != ".lfr":
                print("Unrecognized file Extension")
                sys.exit()

            p = Path(file_path).resolve()
            self.__store_full_text(p)

    def check_syntax_errors(self) -> bool:
        syntax_errors = 0
        for file_path in list(self.resolved_paths.values()):
            print("File: {}".format(file_path))
            finput = FileStream(str(file_path))

            lexer = lfrXLexer(finput)

            stream = CommonTokenStream(lexer)

            parser = lfrXParser(stream)

            parser.skeleton()
            syntax_errors += parser.getNumberOfSyntaxErrors()

        return syntax_errors > 0

    def process(self) -> None:

        dep_graph = nx.DiGraph()
        # add the nodes in the dep graph
        for file_handle in self.full_text:
            dep_graph.add_node(file_handle)

        # We extract his because these are all the files defined by the user
        user_derfined_list = str(self.full_text.keys())

        for file_handle in user_derfined_list:
            # Find all imports and generate the edges
            text = self.full_text[file_handle]
            find_results = re.findall(IMPORT_FILE_PATTERN, text)
            for result in find_results:
                new_file_handle = result[1]
                delete_string = result[0]

                # Check if the file handle is found in the dependency graph
                if new_file_handle not in list(dep_graph.nodes):

                    # Since its not in the dependency graph we check if
                    # its in the preloaded library
                    if new_file_handle not in list(self._lib_file_list.keys()):

                        # Since its not in the preloaded library either...
                        raise Exception("Could not find file - {}".format(result[1]))
                    else:
                        
                        # Pull all the text, add it to the full text store
                        file_path = self._lib_file_list[new_file_handle]
                        p = Path(file_path).resolve()
                        print("Using Library Design at Path: {0}".format(p))
                        self.__store_full_text(p)

                        # Add the file node to the dependency graph here
                        dep_graph.add_node(new_file_handle)

                dep_graph.add_edge(file_handle, new_file_handle)

                text = text.replace(delete_string, "// Removed import")

                self.full_text[file_handle] = text

        ordering = list(reversed(list(nx.topological_sort(dep_graph))))

        final_dump = ""
        print(ordering)
        for file_handle in ordering:
            final_dump += "// Dumping File - {}\n\n\n".format(file_handle)
            final_dump += self.full_text[file_handle]
            final_dump += "\n\n\n\n\n"

        # Generating the Dump
        file = open("pre_processor_dump.lfr", "w")
        file.write(final_dump)
        file.close()

    def __store_full_text(self, file_path: Path):
        """Stores the full text of the give file into the preprocessor store

        Args:
            file_path (Path): Path object of the file
        """
        print("Input Path: {0}".format(file_path))
        # Open a file: file
        file = open(file_path, mode="r")

        # read all lines at once
        all_of_it = file.read()

        # close the file
        file.close()

        self.resolved_paths[file_path.name] = file_path
        self.full_text[file_path.name] = all_of_it
