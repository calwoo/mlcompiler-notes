#include <iostream>
#include "ast.h"


std::ostream& Expr::print(std::ostream& os) const {
    os << "not virtual";
    return os;
}

std::ostream& SExpr::print(std::ostream& os) const {
    os << "[ ";
    for (auto d : data) {
        os << d << " ";
    }
    os << "]";
    return os;
}

// print dispatcher
std::ostream& operator<<(std::ostream& os, const Expr& e) {
    return e.print(os); 
}
