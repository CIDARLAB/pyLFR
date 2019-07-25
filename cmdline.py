import sys
from antlr4 import *
from antlr.lfrXLexer import lfrXLexer
from antlr.lfrXParser import lfrXParser
from lfrCompiler import LFRCompiler
from netlistgenerator.devicegenerator import DeviceGenerator

import argparse


def main():
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

    # Check if the module compilation was successful
    if listener.success:
        # Now Process the Modules Generated
        devicegenerator = DeviceGenerator(listener.currentModule.name, listener.currentModule)
        devicegenerator.generatenetlist()        

if __name__ == "__main__":
    main()


