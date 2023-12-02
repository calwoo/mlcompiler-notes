#include <vector>
#include "parser.h"
#include "ast.h"


std::unique_ptr<Expr> Parser::parse() {
    return expression();
}

std::unique_ptr<Expr> Parser::expression() {
    std::vector<Expr> expressions = std::vector<Expr>();
    return std::make_unique<SExpr>(SExpr(expressions));
}

// helpers
