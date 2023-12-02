#include <iostream>
#include <string>
#include "lexer.h"
#include "parser.h"
#include "ast.h"


int main()
{
    std::string program = "(+ what_ever 3 \"wow\" (* 3 24) \"haha\")";

    Tokenizer tokenizer = Tokenizer(program);

    std::cout << "program: " << program << std::endl;
    std::cout << "lexing:" << std::endl;
    std::vector<Token> tokens = tokenizer.scan();
    for (auto tok : tokens) {
        std::cout << tok << std::endl;
    }

    std::cout << "parsing:" << std::endl;
    Parser parser = Parser(tokens);
    std::unique_ptr<Expr> ast = parser.parse();

    std::cout << *ast << std::endl;

    // Expr e1 = Expr();
    // std::cout << e1 << std::endl;

    // std::vector<Expr> data = std::vector<Expr>();
    // SExpr e2 = SExpr(data);
    // std::cout << e2 << std::endl;

    // Expr e3 = SExpr(data);
    // std::cout << e3 << std::endl;

    return 0;
}
