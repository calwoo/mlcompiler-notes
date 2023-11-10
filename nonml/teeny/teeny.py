import os
from lex import Lexer, TokenType


def main():
    with open(os.path.join(os.path.dirname(__file__), "fib.teeny"), "r") as f:
        source = f.read()

    lexer = Lexer(source)

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.get_token()

if __name__ == "__main__":
    main()
