#pragma once
#include <vector>
#include <iostream>


class Expr {
    public:
        virtual ~Expr() = default;
        virtual std::ostream& print(std::ostream& os) const;
        friend std::ostream& operator<<(std::ostream &out, const Expr& e);
};

class SExpr : public Expr {
    public:
        std::vector<Expr> data;
        SExpr(std::vector<Expr> data) : data(data) {};
        std::ostream& print(std::ostream&) const;
};
