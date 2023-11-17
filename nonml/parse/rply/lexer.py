from rply import LexerGenerator


lg = LexerGenerator()
lg.add("NUMBER", r"\d+")
lg.add("PLUS", r"\+")
lg.add("MINUS", r"-")
lg.add("MUL", r"\*")
lg.add("DIV", r"/")
lg.add("LPARENS", r"\(")
lg.add("RPARENS", r"\)")

# whitespace
lg.ignore(r'\s+')

lexer = lg.build()

if __name__ == "__main__":
    expr = "1 +1"
    for token in lexer.lex(expr):
        print(token)
