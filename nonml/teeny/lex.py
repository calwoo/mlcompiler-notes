import enum
import sys


class Lexer:
    def __init__(self, source):
        self.source = source + "\n"
        self.cur_pos = -1
        self.cur_char = ''
        self.next_char()

    @property
    def length(self):
        return len(self.source)

    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= self.length:
            self.cur_char = '\0' # eof
        else:
            self.cur_char = self.source[self.cur_pos]

    def peek(self):
        """returns lookahead char"""
        if self.cur_pos + 1 >= self.length:
            return '\0'
        else:
            return self.source[self.cur_pos + 1]

    def abort(self, message: str):
        sys.exit(f"lexing error: {message}")

    def skip_whitespace(self):
        pass

    def skip_comment(self):
        pass

    def get_token(self):
        token = None
        if self.cur_char == '+':
            token = Token(self.cur_char, TokenType.PLUS)
        elif self.cur_char == '-':
            token = Token(self.cur_char, TokenType.MINUS)
        elif self.cur_char == '*':
            token = Token(self.cur_char, TokenType.ASTERISK)
        elif self.cur_char == '/':
            token = Token(self.cur_char, TokenType.SLASH)
        elif self.cur_char == '\n':
            token = Token(self.cur_char, TokenType.NEWLINE)
        elif self.cur_char == '\0':
            token = Token('', TokenType.EOF)
        else:
            # dunno
            self.abort(f"unknown token {self.cur_char}")

        self.next_char()
        return token


class Token:
    def __init__(self, text, kind):
        self.text = text
        self.kind = kind


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # keywords
    LABEL = 4
    GOTO = 5
    PRINT = 6
    INPUT = 7
    LET = 8
    IF = 9
    THEN = 10
    ENDIF = 11
    WHILE = 12
    REPEAT = 13
    ENDWHILE = 14
	# algebraic ops
    EQ = 15
    PLUS = 16
    MINUS = 17
    ASTERISK = 18
    SLASH = 19
    EQEQ = 20
    NOTEQ = 21
    LT = 22
    LTEQ = 23
    GT = 24
    GTEQ = 25
