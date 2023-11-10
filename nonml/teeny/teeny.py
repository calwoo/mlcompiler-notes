import os
import sys

from lex import Lexer, TokenType
from parse import Parser


def main():
    if len(sys.argv) != 2:
        sys.exit("error: compiler needs source")
    with open(os.path.abspath(sys.argv[1]), "r") as f:
        source = f.read()

    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program()
    print("parsing finished")

if __name__ == "__main__":
    main()
