from lex import Lexer, TokenType


def main():
    # source = "LET foobar = 123"
    source = "+- */ >>= = !=" 
    lexer = Lexer(source)

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.get_token()

if __name__ == "__main__":
    main()
