import sys
from lex import TokenType


class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter
        
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
        self.emitter.header_line("#include <stdio.h>")
        self.emitter.header_line("int main(void) {")

        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()

        self.emitter.emit_line("return 0;")
        self.emitter.emit_line("}")

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
            self.next_token()
            if self.check_token(TokenType.STRING):
                self.emitter.emit_line(f"printf(\"{self.cur_token.text}\\n\");")
                self.next_token()
            else:
                self.emitter.emit("printf(\"%.2f\\n\", (float)(")
                self.expression()
                self.emitter.emit_line("));")
        # "IF" comparison "THEN" nl {statement} "ENDIF"
        elif self.check_token(TokenType.IF):
            self.next_token()
            self.emitter.emit("if (")
            self.comparison()

            self.match(TokenType.THEN)
            self.newline()
            self.emitter.emit_line(") {")

            while not self.check_token(TokenType.ENDIF):
                self.statement()
            
            self.match(TokenType.ENDIF)
            self.emitter.emit_line("}")
        # "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE"
        elif self.check_token(TokenType.WHILE):
            self.next_token()
            self.emitter.emit("while (")
            self.comparison()

            self.match(TokenType.REPEAT)
            self.newline()
            self.emitter.emit_line(") {")

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emit_line("}")
        # "LABEL" ident
        elif self.check_token(TokenType.LABEL):
            self.next_token()

            if self.cur_token.text in self.labels_declared:
                self.abort(f"label already exists: {self.cur_token.text}")
            self.labels_declared.add(self.cur_token.text)

            self.emitter.emit_line(f"{self.cur_token.text}:")
            self.match(TokenType.IDENT)
        # "GOTO" ident
        elif self.check_token(TokenType.GOTO):
            self.next_token()
            self.labels_gotoed.add(self.cur_token.text)
            self.emitter.emit_line(f"goto {self.cur_token.text};")
            self.match(TokenType.IDENT)
        # "LET" ident "=" expression
        elif self.check_token(TokenType.LET):
            self.next_token()

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.header_line(f"float {self.cur_token.text};")

            self.emitter.emit(f"{self.cur_token.text} = ")
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
            self.emitter.emit_line(";")
        # "INPUT" ident
        elif self.check_token(TokenType.INPUT):
            self.next_token()

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.header_line(f"float {self.cur_token.text};")
    
            self.emitter.emit_line("if (0 == scanf(\"%f\", &" + self.cur_token.text + ")) {")
            self.emitter.emit_line(f"{self.cur_token.text} = 0;")
            self.emitter.emit_line(f"scanf(\"%*s\");")
            self.emitter.emit_line("}")
            self.match(TokenType.IDENT)
        else:
            self.abort(f"invalid statement at {self.cur_token.text}:({self.cur_token.kind.name})")

        self.newline()

    def comparison(self):
        """
        comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
        """
        self.expression()
        if self.is_comparison_operator():
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.expression()
        else:
            self.abort(f"expected comparison operator at {self.cur_token.text}")

        while self.is_comparison_operator():
            self.emitter.emit(self.cur_token.text)
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
        self.term()
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.term()

    def term(self):
        """
        term ::= unary {( "/" | "*" ) unary}
        """
        self.unary()
        while self.check_token(TokenType.SLASH) or self.check_token(TokenType.ASTERISK):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.unary()

    def unary(self):
        """
        unary ::= ["+" | "-"] primary
        """
        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        self.primary()

    def primary(self):
        """
        primary ::= number | ident
        """
        if self.check_token(TokenType.NUMBER):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            if self.cur_token.text not in self.symbols:
                self.abort(f"referencing variable before assignment: {self.cur_token.text}")
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        else:
            self.abort(f"unexpected token at {self.cur_token.text}")

    def newline(self):
        """
        nl ::= '\n'+
        """
        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()
