import os
import sys

from lex import Lexer
from parse import Parser
from emit import *


def main():
    if len(sys.argv) != 2:
        sys.exit("error: compiler needs source")
    with open(os.path.abspath(sys.argv[1]), "r") as f:
        source = f.read()

    lexer = Lexer(source)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()
    emitter.write_file()
    print("compiling finished")

if __name__ == "__main__":
    main()
