def eval(exp):
    if is_number(exp):
        return exp
    if is_string(exp):
        return exp[1:-1]
    if exp[0] == '+':
        return eval(exp[1]) + eval(exp[2])
    raise NotImplementedError

def is_number(exp):
    return isinstance(exp, int) or isinstance(exp, float)

def is_string(exp):
    # strings have to be delimited by double quotes ""
    return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'
