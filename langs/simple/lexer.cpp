#include <iostream>
#include <regex>
#include <vector>
#include <string>
#include <string_view>
#include "token.h"
#include "lexer.h"


std::vector<Token> Tokenizer::scan() {
    std::string_view s{source};

    while (current_offset < source.size()) {
        char curr_ch = source[current_offset];

        // parentheses
        if (curr_ch == '(') {
            tokens.push_back(Token(TokenType::LPAREN));
        } else if (curr_ch == ')') {
            tokens.push_back(Token(TokenType::RPAREN));
        }
        // numbers
        else if (is_digit(curr_ch)) {
            while ((current_offset + 1 < source.size()) && is_digit(source[current_offset + 1])) {
                current_offset += 1;
            }

            int number_len = current_offset - start_offset + 1;
            tokens.push_back(
                Token(TokenType::NUMBER, source.substr(start_offset, number_len))
            );
        }
        // strings
        else if (curr_ch == '"') {
            while ((current_offset + 1 < source.size()) && (source[current_offset + 1] != '"')) {
                current_offset += 1;
            }

            int string_len = current_offset - start_offset;
            tokens.push_back(
                Token(TokenType::STRING, source.substr(start_offset + 1, string_len))
            );
            // consume the closing "
            current_offset += 1;
        }
        // identifiers
        else if (is_symb(curr_ch)) {
            while ((current_offset + 1 < source.size()) && is_symb(source[current_offset + 1])) {
                current_offset += 1;
            }

            int symbol_len = current_offset - start_offset + 1;
            tokens.push_back(
                Token(TokenType::IDENTIFIER, source.substr(start_offset, symbol_len))
            );
        }

        current_offset += 1;
        start_offset = current_offset;
    }

    return tokens;
}

bool is_digit(const char& ch) {
    return ch >= '0' && ch <= '9';
}

bool is_symb(const char& ch) {
    switch (ch) {
        case '+':
        case '-':
        case '*':
        case '/':
            return true;
    }

    std::string str(1, ch);
    std::regex pattern("[a-zA-Z_]");
    return std::regex_match(str, pattern);
}
