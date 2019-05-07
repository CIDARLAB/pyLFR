import sys
from antlr4 import *
from antlr.lfrXLexer import lfrXLexer
from antlr.lfrXParser import lfrXParser
from lfrCompiler import LFRCompiler

import argparse


parser = argparse.ArgumentParser()

parser.add_argument('input', help="this is the file thats used as the input ")

args = parser.parse_args()

print(args.input)

finput = FileStream(args.input)

lexer = lfrXLexer(finput)

stream = CommonTokenStream(lexer)

parser = lfrXParser(stream)

tree = parser.skeleton()

walker = ParseTreeWalker()

listener = LFRCompiler()

walker.walk(listener, tree)


