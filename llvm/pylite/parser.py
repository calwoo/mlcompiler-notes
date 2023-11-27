from rply import ParserGenerator
import ast


class Parser:
    def __init__(self, codegen):
        module = codegen.module
        builder = codegen.builder
        printf_fn = codegen.printf

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
            return ast.Print(module, builder, printf_fn, p[2])
        
        @pg.production("expression : expression PLUS expression")
        @pg.production("expression : expression MINUS expression")
        def expression(p):
            left, op, right = p
            if op.gettokentype() == "PLUS":
                return ast.Sum(module, builder, left, right)
            elif op.gettokentype() == "MINUS":
                return ast.Sub(module, builder, left, right)
            
        @pg.production("expression : NUMBER")
        def number(p):
            return ast.Number(module, builder, p[0].value)
        
        @pg.error
        def error(token):
            raise ValueError(f"invalid token: {token}")
        
        self.pg = pg.build()
        
    def parse(self, tokens):
        return self.pg.parse(tokens)
