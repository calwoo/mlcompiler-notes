#include <iostream>
#include <string>
#include "lexer.h"


int main()
{
    std::string program = "(+ what_ever 3 \"wow\" (* 3 24) \"haha\")";

    Tokenizer tokenizer = Tokenizer(program);

    std::cout << "parsing: " << program << std::endl;
    std::vector<Token> tokens = tokenizer.scan();
    for (auto tok : tokens) {
        std::cout << tok << std::endl;
    }

    return 0;
}