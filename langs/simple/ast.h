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
        std::vector<std::unique_ptr<Expr>> data;
        SExpr(std::vector<std::unique_ptr<Expr>> data) : 
            data(std::move(data)) {};
        std::ostream& print(std::ostream& os) override;
};

class IdenExpr : public Expr {
    public:
        std::string name;
        IdenExpr(std::string& name) : name(name) {};
        std::ostream& print(std::ostream& os) override;
};

class NumExpr : public Expr {
    public:
        double value;
        NumExpr(double value) : value(value) {};
        std::ostream& print(std::ostream& os) override;
};

class StrExpr : public Expr {
    public:
        std::string value;
        StrExpr(std::string& value) : value(value) {};
        std::ostream& print(std::ostream& os) override;
};
