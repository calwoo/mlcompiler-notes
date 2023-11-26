#include <iostream>
#include <string>
#include "token.h"


std::ostream& operator<<(std::ostream &out, const Token& data) {
    if (data.type == TokenType::NUMBER) {
        out << "NUMBER: " << data.lexeme;
    } else if (data.type == TokenType::STRING) {
        out << "STRING: " << data.lexeme;
    } else if (data.type == TokenType::IDENTIFIER) {
        out << "IDENTIFIER: " << data.lexeme;
    } else if (data.type == TokenType::LPAREN) {
        out << "LPAREN";
    } else if (data.type == TokenType::RPAREN) {
        out << "RPAREN";
    } else {
        out << "UNKNOWN!";
    }

    return out;
}
