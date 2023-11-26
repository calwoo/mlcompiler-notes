#pragma once

#include "token.h"
#include <string>
#include <vector>

class Tokenizer {
    private:
        std::string source;
        std::vector<Token> tokens;

        int start_offset = 0;
        int current_offset = 0;

    public:
        Tokenizer(const std::string& source)
            : source(source), tokens(std::vector<Token>()) {}
        
        std::vector<Token> scan();
};

// utility functions
bool is_digit(const char& ch);
bool is_symb(const char& ch);
