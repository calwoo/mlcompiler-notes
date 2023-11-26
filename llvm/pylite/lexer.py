from rply import LexerGenerator


class Lexer:
    def __init__(self):
        lexer = LexerGenerator()
        # tokens
        lexer.add("PRINT", r"print")
        lexer.add("LPAREN", r"\(")
        lexer.add("RPAREN", r"\)")
        lexer.add("SEMICOLON", r"\;")
        lexer.add("PLUS", r"\+")
        lexer.add("MINUS", r"\-")
        lexer.add("NUMBER", r"\d+")
        lexer.ignore("\s+")
        # build lexer
        self.lexer = lexer.build()

    def tokenize(self, source):
        return self.lexer.lex(source)
