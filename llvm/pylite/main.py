from lexer import Lexer
from parser import Parser


lexer = Lexer()
parser = Parser()

if __name__ == "__main__":
    with open("test.toy", "r") as f:
        source = f.read()

    tokens = lexer.tokenize(source)
    ast = parser.parse(tokens)

    ast.eval()
