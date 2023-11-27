from lexer import Lexer
from parser import Parser
from codegen import CodeGen


lexer = Lexer()
codegen = CodeGen()
parser = Parser(codegen)

if __name__ == "__main__":
    with open("test.toy", "r") as f:
        source = f.read()

    tokens = lexer.tokenize(source)
    ast = parser.parse(tokens)

    ast.eval()

    print(codegen.compile())
    codegen.save_ir()
