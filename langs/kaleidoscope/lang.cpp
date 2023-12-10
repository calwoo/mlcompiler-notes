#include <cstdio>
#include <string>
#include <vector>
#include <map>
#include <memory>

// lexer
enum Token {
    tok_eof = -1,
    tok_def = -2,
    tok_extern = -3,
    tok_identifier = -4,
    tok_number = -5
};

static std::string id_str;
static double num_val;

// gettok: return next token from stdin
static int gettok() {
    static int last_char = ' ';
    // skip whitespace
    while (isspace(last_char))
        last_char = getchar();
    // recognize identifier
    if (isalpha(last_char)) {
        id_str = last_char;
        while (isalnum((last_char = getchar())))
            id_str += last_char;

        if (id_str == "def")
            return tok_def;
        if (id_str == "extern")
            return tok_extern;
        return tok_identifier;
    }
    // numbers
    if (isdigit(last_char) || last_char == '.') {
        std::string num_str;
        do {
            num_str += last_char;
            last_char = getchar();
        } while (isdigit(last_char) || last_char == '.');

        num_val = strtod(num_str.c_str(), 0);
        return tok_number;
    }
    // comments
    if (last_char == '#') {
        do
            last_char = getchar();
        while (last_char != EOF && last_char != '\n' && last_char != '\r');

        if (last_char != EOF)
            return gettok();
    }
    // eof
    if (last_char == EOF)
        return tok_eof;

    int this_char = last_char;
    last_char = getchar();
    return this_char;    
}

class ExprAST {
    public:
        virtual ~ExprAST() = default;
};

class NumberExprAST : public ExprAST {
    double val;
    public:
        NumberExprAST(double val) : val(val) {}
};

class VariableExprAST : public ExprAST {
    std::string name;
    public:
        VariableExprAST(const std::string& name) : name(name) {}
};

class BinaryExprAST : public ExprAST {
    char op;
    std::unique_ptr<ExprAST> LHS, RHS;

    public:
        BinaryExprAST(char op, std::unique_ptr<ExprAST> LHS, std::unique_ptr<ExprAST> RHS)
            : op(op), LHS(std::move(LHS)), RHS(std::move(RHS)) {}
};

class CallExprAST : public ExprAST {
    std::string callee;
    std::vector<std::unique_ptr<ExprAST>> args;

    public:
        CallExprAST(const std::string& callee,
                    std::vector<std::unique_ptr<ExprAST>> args)
            : callee(callee), args(std::move(args)) {}
};

class PrototypeAST {
    std::string name;
    std::vector<std::string> args;

    public:
        PrototypeAST(const std::string& name, std::vector<std::string> args)
            : name(name), args(std::move(args)) {}
        const std::string& get_name() const { return name; }
};

class FunctionAST {
    std::unique_ptr<PrototypeAST> proto;
    std::unique_ptr<ExprAST> body;

    public:
        FunctionAST(std::unique_ptr<PrototypeAST> proto,
                    std::unique_ptr<ExprAST> body)
            : proto(std::move(proto)), body(std::move(body)) {}
};

static int cur_tok;
static int get_next_token() {
    return cur_tok = gettok();
}

/// LogError* - These are little helper functions for error handling.
std::unique_ptr<ExprAST> log_error(const char *Str) {
    fprintf(stderr, "Error: %s\n", Str);
    return nullptr;
}
std::unique_ptr<PrototypeAST> log_errorp(const char *Str) {
    LogError(Str);
    return nullptr;
}

// numberexpr ::= number
static std::unique_ptr<ExprAST> parse_number_expr() {
    auto result = std::make_unique<NumberExprAST>(num_val);
    get_next_token();
    return std::move(result);
}

// parenexpr ::= '(' expr ')'
static std::unique_ptr<ExprAST> parse_paren_expr() {
    get_next_token();
    auto v = parse_expression();
    if (!v) return nullptr;
    if (cur_tok != ')')
        return log_error("expected ')'");
    get_next_token();
    return v;
}

