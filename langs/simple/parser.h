#pragma once

#include "token.h"
#include "ast.h"
#include <vector>

class Parser {
    private:
        std::vector<Token> tokens;
        int current;
    
    public:
        Parser(std::vector<Token>& tokens) : tokens(tokens), current(0) {};
        std::unique_ptr<Expr> parse();
        std::unique_ptr<Expr> expression();
        std::unique_ptr<Expr> number();
        std::unique_ptr<Expr> string();
        std::unique_ptr<Expr> identifier();
        Token peek();
        bool consume();
};
