#pragma once
#include <vector>
#include <string>
#include <iostream>


class Expr {
    public:
        virtual ~Expr() = default;
        virtual std::ostream& print(std::ostream& os);
        friend std::ostream& operator<<(std::ostream& out, Expr& e) {
            return e.print(out);
        }
};

class SExpr : public Expr {
    public:
        std::vector<Expr> data;
        SExpr(std::vector<Expr>& data) : data(data) {};
        std::ostream& print(std::ostream& os) override;
};

class IdenExpr : public Expr {
    public:
        std::string name;
        IdenExpr(std::string& name) : name(name) {};
        std::ostream& print(std::ostream& os) override;
};
