#include <string>
#include <vector>


enum class ExpType {
    NUMBER,
    STRING,
    SYMBOL,
    LIST,
};

/**
 * expressions
*/
class Exp {
    public:
        ExpType type;

        int number;
        std::string string;
        std::vector<Exp> list;

        // numbers
        Exp(int number) : type(ExpType::NUMBER), number(number) {}

        // strings, symbols
        Exp(const std::string& strVal) {
            if (strVal[0] == '"') {
                type = ExpType::STRING;
                string = strVal.substr(1, strVal.size() - 2);
            } else {
                type = ExpType::SYMBOL;
                string = strVal;
            }
        }

        // list
        Exp(std::vector<Exp> list) : type(ExpType::LIST), list(list) {}
};

using Value = Exp;
