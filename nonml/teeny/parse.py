import sys
from lex import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # initialize twice
        self.cur_token = lexer.get_token()
        self.peek_token = lexer.get_token()

    def check_token(self, kind) -> bool:
        return kind == self.cur_token.kind

    def check_peek(self, kind) -> bool:
        return kind == self.peek_token.kind

    def match(self, kind):
        if not self.check_token(kind):
            self.abort(f"expected {kind.name}, but got {self.cur_token.kind} instead")
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message: str):
        sys.exit(f"error: {message}")

    def program(self):
        pass
