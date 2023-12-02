#include <vector>
#include <csignal>
#include "token.h"
#include "parser.h"
#include "ast.h"


std::unique_ptr<Expr> Parser::parse() {
    return expression();
}

std::unique_ptr<Expr> Parser::expression() {
    std::vector<Expr> expressions = std::vector<Expr>();
    consume(TokenType::LPAREN);

    Token curr_token = tokens[current];
    while (curr_token.type != TokenType::RPAREN) {
        switch (curr_token.type) {
            case TokenType::LPAREN:
                expression();
                break;
            case TokenType::IDENTIFIER:
                identifier();
                break;
            case TokenType::NUMBER:
                number();
                break;
            // case TokenType::STRING:
            //     string();
            //     break;
            default:
                std::cout << curr_token << std::endl;
                std::raise(SIGTERM);
        }
        curr_token = tokens[current];
    }

    consume(TokenType::RPAREN);

    return std::make_unique<SExpr>(SExpr(expressions));
}

std::unique_ptr<Expr> Parser::identifier() {
    Token curr_token = tokens[current];
    IdenExpr expr = IdenExpr(curr_token.lexeme);
    current++;  // advance the index
    return std::make_unique<IdenExpr>(expr);
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
