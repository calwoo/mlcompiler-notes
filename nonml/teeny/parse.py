import sys
from lex import TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        
        self.symbols = set()
        self.labels_declared = set()
        self.labels_gotoed = set()
        # initialize twice
        self.cur_token = lexer.get_token()
        self.peek_token = lexer.get_token()

    def check_token(self, kind) -> bool:
        return kind == self.cur_token.kind

    def check_peek(self, kind) -> bool:
        return kind == self.peek_token.kind

    def match(self, kind):
        if not self.check_token(kind):
            self.abort(f"expected {kind.name}, but got {self.cur_token.kind.name} instead")
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message: str):
        sys.exit(f"error: {message}")

    def program(self):
        """
        program ::= {statement}
        """
        print("PROGRAM")

        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()

        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort(f"attempting to GOTO undeclared label: {label}")

    def statement(self):
        """
        statement ::= "PRINT" (expression | string) nl
            | "IF" comparison "THEN" nl {statement} "ENDIF" nl
            | "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
            | "LABEL" ident nl
            | "GOTO" ident nl
            | "LET" ident "=" expression nl
            | "INPUT" ident nl
        """
        # "PRINT" (expression | string)
        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()
            if self.check_token(TokenType.STRING):
                self.next_token()
            else:
                self.expression()
        # "IF" comparison "THEN" nl {statement} "ENDIF"
        elif self.check_token(TokenType.IF):
            print("STATEMENT-IF")
            self.next_token()
            self.comparison()

            self.match(TokenType.THEN)
            self.newline()

            while not self.check_token(TokenType.ENDIF):
                self.statement()
            
            self.match(TokenType.ENDIF)
        # "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE"
        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.newline()

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
        # "LABEL" ident
        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.next_token()

            if self.cur_token.text in self.labels_declared:
                self.abort(f"label already exists: {self.cur_token.text}")
            self.labels_declared.add(self.cur_token.text)

            self.match(TokenType.IDENT)
        # "GOTO" ident
        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.next_token()
            self.labels_gotoed.add(self.cur_token.text)
            self.match(TokenType.IDENT)
        # "LET" ident "=" expression
        elif self.check_token(TokenType.LET):
            print("STATEMENT-LET")
            self.next_token()

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
        # "INPUT" ident
        elif self.check_token(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.next_token()

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)

            self.match(TokenType.IDENT)
        else:
            self.abort(f"invalid statement at {self.cur_token.text}:({self.cur_token.kind.name})")

        self.newline()

    def comparison(self):
        """
        comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
        """
        print("COMPARISON")
        
        self.expression()
        if self.is_comparison_operator():
            self.next_token()
            self.expression()
        else:
            self.abort(f"expected comparison operator at {self.cur_token.text}")

        while self.is_comparison_operator():
            self.next_token()
            self.expression()

    def is_comparison_operator(self):
        return (
            self.check_token(TokenType.EQEQ)
            or self.check_token(TokenType.NOTEQ)
            or self.check_token(TokenType.GT)
            or self.check_token(TokenType.GTEQ)
            or self.check_token(TokenType.LT)
            or self.check_token(TokenType.LTEQ)
        )
    
    def expression(self):
        """
        expression ::= term {( "-" | "+" ) term}
        """
        print("EXPRESSION")

        self.term()
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
            self.term()

    def term(self):
        """
        term ::= unary {( "/" | "*" ) unary}
        """
        print("TERM")

        self.unary()
        while self.check_token(TokenType.SLASH) or self.check_token(TokenType.ASTERISK):
            self.next_token()
            self.unary()

    def unary(self):
        """
        unary ::= ["+" | "-"] primary
        """
        print("UNARY")

        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
        self.primary()

    def primary(self):
        """
        primary ::= number | ident
        """
        print(f"PRIMARY ({self.cur_token.text})")

        if self.check_token(TokenType.NUMBER):
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            if self.cur_token.text not in self.symbols:
                self.abort(f"referencing variable before assignment: {self.cur_token.text}")
            self.next_token()
        else:
            self.abort(f"unexpected token at {self.cur_token.text}")

    def newline(self):
        """
        nl ::= '\n'+
        """
        print("NEWLINE")
        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()
