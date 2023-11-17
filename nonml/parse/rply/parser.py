"""
<main> ::= <expr>
<expr> ::= "\d+"
         | <expr> "+" <expr>
         | <expr> "-" <expr>
         | <expr> "*" <expr>
         | <expr> "/" <expr>
         | "(" <expr> ")"
"""

from lexer import lexer
from rply import ParserGenerator
from rply.token import BaseBox

# ast
class Number(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value
    
class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()
    
class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()

class Mul(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()
    
class Div(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()
    
# parser
pg = ParserGenerator(
    ["NUMBER", "PLUS", "MINUS", "MUL", "DIV", "LPARENS", "RPARENS"],
    precedence=[
        ("left", ["PLUS", "MINUS"]),
        ("left", ["MUL", "DIV"])
    ]
)

@pg.production("main : expr")
def main(p):
    return p[0]

@pg.production("expr : NUMBER")
def expr_number(p):
    # print(p)
    return Number(int(p[0].getstr()))

@pg.production("expr : LPARENS expr RPARENS")
def expr_parens(p):
    return p[1]

@pg.production("expr : expr PLUS expr")
@pg.production("expr : expr MINUS expr")
@pg.production("expr : expr MUL expr")
@pg.production("expr : expr DIV expr")
def expr_binop(p):
    # print(p)
    left = p[0]
    right = p[2]
    if p[1].gettokentype() == "PLUS":
        return Add(left, right)
    elif p[1].gettokentype() == 'MINUS':
        return Sub(left, right)
    elif p[1].gettokentype() == 'MUL':
        return Mul(left, right)
    elif p[1].gettokentype() == 'DIV':
        return Div(left, right)
    else:
        raise Exception("not valid")

parser = pg.build()


if __name__ == "__main__":
    expr = "(2 + 3) * (3 * (4 - 3))"
    tokens = lexer.lex(expr)
    print(parser.parse(tokens).eval())
