from rply import ParserGenerator
import ast


class Parser:
    def __init__(self):
        pg = ParserGenerator([
            "PRINT",
            "LPAREN",
            "RPAREN",
            "SEMICOLON",
            "PLUS",
            "MINUS",
            "NUMBER",
        ])

        @pg.production("program : PRINT LPAREN expression RPAREN SEMICOLON")
        def program(p):
            return ast.Print(p[2])
        
        @pg.production("expression : expression PLUS expression")
        @pg.production("expression : expression MINUS expression")
        def expression(p):
            left, op, right = p
            if op.gettokentype() == "PLUS":
                return ast.Sum(left, right)
            elif op.gettokentype() == "MINUS":
                return ast.Sub(left, right)
            
        @pg.production("expression : NUMBER")
        def number(p):
            return ast.Number(p[0].value)
        
        @pg.error
        def error(token):
            raise ValueError(f"invalid token: {token}")
        
        self.pg = pg.build()
        
    def parse(self, tokens):
        return self.pg.parse(tokens)
