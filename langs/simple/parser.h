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
        Expr parse();
        Expr expression();
        Expr number();
        Expr string();
        Expr identifier();
        Token peek();
        bool consume();
};
