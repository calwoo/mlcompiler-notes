#include <vector>
#include <csignal>
#include "token.h"
#include "parser.h"
#include "ast.h"


std::unique_ptr<Expr> Parser::parse() {
    return expression();
}

std::unique_ptr<Expr> Parser::expression() {
    std::vector<std::unique_ptr<Expr>> expressions = 
        std::vector<std::unique_ptr<Expr>>();
    consume(TokenType::LPAREN);

    Token curr_token = tokens[current];
    std::unique_ptr<Expr> captured_expr;
    while (curr_token.type != TokenType::RPAREN) {
        switch (curr_token.type) {
            case TokenType::LPAREN:
                captured_expr = expression();
                break;
            case TokenType::IDENTIFIER:
                captured_expr = identifier();
                break;
            case TokenType::NUMBER:
                captured_expr = number();
                break;
            case TokenType::STRING:
                captured_expr = string();
                break;
            default:
                std::cout << curr_token << std::endl;
                std::raise(SIGTERM);
        }
        expressions.push_back(std::move(captured_expr));
        curr_token = tokens[current];
    }

    consume(TokenType::RPAREN);

    SExpr expr = SExpr(std::move(expressions));
    return std::make_unique<SExpr>(std::move(expr));
}

std::unique_ptr<Expr> Parser::identifier() {
    Token curr_token = tokens[current];
    IdenExpr expr = IdenExpr(curr_token.lexeme);
    current++;  // advance the index
    return std::make_unique<IdenExpr>(expr);
}

std::unique_ptr<Expr> Parser::number() {
    Token curr_token = tokens[current];
    NumExpr expr = NumExpr(std::stod(curr_token.lexeme));
    current++;  // advance the index
    return std::make_unique<NumExpr>(expr);
}

std::unique_ptr<Expr> Parser::string() {
    Token curr_token = tokens[current];
    StrExpr expr = StrExpr(curr_token.lexeme);
    current++;  // advance the index
    return std::make_unique<StrExpr>(expr);
}

// helpers
Token Parser::peek() {
    if (current + 1 < tokens.size()) {
        return tokens[current + 1];
    }
    return Token(TokenType::ENDFILE);
}

void Parser::consume(TokenType t) {
    Token curr_token = tokens[current];
    if (t != curr_token.type) {
        std::raise(SIGTERM);
    }
    current++;
}
