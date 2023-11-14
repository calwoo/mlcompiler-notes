def tokenize(s_expr: str) -> list:
    tokens = s_expr.replace('(', " ( ").replace(')', " ) ").split()
    return tokens

def singleton(token: str):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token

def parse_as_tree(tokens: list[str]) -> list:
    if len(tokens) == 0:
        raise SyntaxError("unexpected eof")
    token = tokens.pop(0)
    if token == "(":
        # create new stack frame
        exp = []
        while tokens[0] != ")":
            nested_exp_or_singleton = parse_as_tree(tokens)
            exp.append(nested_exp_or_singleton)
        # pop closing paren
        tokens.pop(0)
        return exp
    elif token == ")":
        raise SyntaxError("unexpected closing paren")
    else:
        return singleton(token)

def parse(s_expr):
    tokens = tokenize(s_expr)
    return parse_as_tree(tokens)


if __name__ == "__main__":
    s_expr = "(+ (* 2 3) 5)"
    print(parse(s_expr))

    s_expr = """
    (begin
        (var x 10)
        (var y 20)
        (if (> x 10)
            (set y 20)
            (set y 30))
        y
    )
    """
    print(parse(s_expr))
