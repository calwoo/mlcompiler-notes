#include <vector>
#include "parser.h"
#include "ast.h"


Expr Parser::parse() {
    return expression();
}

Expr Parser::expression() {
    std::vector<Expr> expressions = std::vector<Expr>();
    return SExpr(expressions);
}

// helpers
