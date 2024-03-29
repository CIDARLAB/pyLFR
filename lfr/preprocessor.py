import re
import sys
from pathlib import Path
from typing import List

import networkx as nx
from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.FileStream import FileStream

from lfr.antlrgen.lfrXLexer import lfrXLexer
from lfr.antlrgen.lfrXParser import lfrXParser

IMPORT_FILE_PATTERN = r"(`import\s+\"(\w+.lfr)\")"


class PreProcessor:
    def __init__(self, file_list: List[str]) -> None:
        self.resolved_paths = {}
        self.full_text = {}
        self.text_dump = None
        for file_path in file_list:

            extension = Path(file_path).suffix
            if extension != ".lfr":
                print("Unrecognized file Extension")
                sys.exit()

            p = Path(file_path).resolve()
            print("Input Path: {0}".format(p))
            # Open a file: file
            file = open(p, mode="r")

            # read all lines at once
            all_of_it = file.read()

            # close the file
            file.close()

            self.resolved_paths[p.name] = p
            self.full_text[p.name] = all_of_it

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

        for file_handle in self.full_text:
            # Find all imports and generate the edges
            text = self.full_text[file_handle]
            find_results = re.findall(IMPORT_FILE_PATTERN, text)
            for result in find_results:
                new_file_handle = result[1]
                delete_string = result[0]

                if new_file_handle not in list(dep_graph.nodes):
                    raise Exception("Could not find file - {}".format(result[1]))

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
