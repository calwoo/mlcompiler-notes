#pragma once
#include <iostream>
#include <string>

enum TokenType {
    IDENTIFIER,
    NUMBER,
    STRING,
    LPAREN,
    RPAREN,
};

class Token {
    public:
        TokenType type;
        std::string lexeme;
        Token(TokenType type, const std::string& lexeme)
            : type(type), lexeme(lexeme) {}
        Token(TokenType type) : type(type) {}

        friend std::ostream& operator<<(std::ostream &out, const Token& data);
};
