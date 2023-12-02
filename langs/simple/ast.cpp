#include <iostream>
#include "ast.h"


std::ostream& Expr::print(std::ostream& os) {
    os << "not virtual";
    return os;
}

std::ostream& SExpr::print(std::ostream& os) {
    os << "[ ";
    for (auto d : data) {
        os << d << " ";
    }
    os << "]";
    return os;
}

std::ostream& IdenExpr::print(std::ostream& os) {
    os << name << ":id";
    return os;
}
