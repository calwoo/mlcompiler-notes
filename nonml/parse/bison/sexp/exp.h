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
struct Exp {
    ExpType type;

    int number;
    std::string string;
    std::vector<Exp> list;
};
