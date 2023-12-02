#include <iostream>
#include "ast.h"


std::ostream& Expr::print(std::ostream& os) {
    os << "not virtual";
    return os;
}

std::ostream& SExpr::print(std::ostream& os) {
    os << "[ ";
    for (auto const& d : data) {
        os << *d << " ";
    }
    os << "]";
    return os;
}

std::ostream& IdenExpr::print(std::ostream& os) {
    os << name << ":id";
    return os;
}

std::ostream& NumExpr::print(std::ostream& os) {
    os << value << ":num";
    return os;
}

std::ostream& StrExpr::print(std::ostream& os) {
    os << value << ":str";
    return os;
}
