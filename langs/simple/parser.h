#pragma once

#include "token.h"
#include <vector>

class Parser {
    private:
        std::vector<Token> tokens;
        int current;
    
    public:
        Parser(std::vector<Token>& tokens) : tokens(tokens), current(0) {};
};
