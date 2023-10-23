from __future__ import annotations

from typing import Dict

from antlr4 import InputStream
from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.tree.Tree import ParseTreeWalker
from networkx.classes.digraph import DiGraph

from lfr.antlrgen.reggie.reggieLexer import reggieLexer
from lfr.antlrgen.reggie.reggieParser import reggieParser
from lfr.graphmatch.matchpatterngenerator import MatchPatternGenerator
from lfr.graphmatch.nodefilter import NodeFilter


class MatchPattern:
    def __init__(self, pattern_string: str = "") -> None:
        if pattern_string == "" or pattern_string is None:
            raise Exception("Empty Pattern found")

        self.__pattern_string = pattern_string
        self._structural_template = None

        # Dictionary that stores the nodefilter object and the node id
        self._semantic_template: Dict[str, NodeFilter] = {}

        self.__parse_pattern(pattern_string)

    def get_structural_template(self) -> DiGraph:
        if self._structural_template is None:
            raise Exception("No structural template assigned")

        return self._structural_template

    def get_semantic_template(self) -> Dict[str, NodeFilter]:
        return self._semantic_template

    def __parse_pattern(self, pattern) -> None:
        # Implement the reggie parser walker, execution of the compiler
        # Step 1 - Parse the thing
        # Step 2 - Save the structural Template
        # Step 3 - Save the semantic template
        istream = InputStream(pattern)
        lexer = reggieLexer(istream)
        stream = CommonTokenStream(lexer)
        parser = reggieParser(stream)

        syntax_errors = parser.getNumberOfSyntaxErrors()
        if syntax_errors > 0:
            raise Exception(
                "Could not parse the match expression, interrupting parsing flow"
            )

        tree = parser.graph()
        walker = ParseTreeWalker()
        listener = MatchPatternGenerator()

        walker.walk(listener, tree)

        self._structural_template = listener.structural_template
        self._semantic_template = listener.semantic_template
