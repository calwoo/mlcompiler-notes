#include <iostream>
#include <string>
#include "lexer.h"
#include "parser.h"


int main()
{
    std::string program = "(+ what_ever 3 \"wow\" (* 3 24) \"haha\")";

    Tokenizer tokenizer = Tokenizer(program);

    std::cout << "parsing: " << program << std::endl;
    std::vector<Token> tokens = tokenizer.scan();
    for (auto tok : tokens) {
        std::cout << tok << std::endl;
    }

    Parser parser = Parser(tokens);
    auto ast = parser.parse();

    std::cout << ast << std::endl;

    return 0;
}
