import math
import operator as op


# typedefs
Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)

# environment
class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer
    
    def find(self, var):
        # search inner first, then outer
        if var in self:
            return self
        else:
            return self.outer.find(var)
        
class Procedure:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval(self.body, env=Env(self.params, args, self.env))

def baseenv() -> Env:
    env = Env()
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv, 
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'expt':    pow,
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: List(x), 
        'list?':   lambda x: isinstance(x, List), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),  
		'print':   print,
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = baseenv()

def tokenize(program: str) -> list:
    return program.replace('(', ' ( ').replace(')', ' ) ').split()

def singleton(token: str) -> Atom:
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

def parse_as_tree(tokens: list[str]) -> list[Exp]:
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

def parse(program: str) -> list[str]:
    tokens = tokenize(program)
    ast = parse_as_tree(tokens)
    return ast

def eval(ast: Exp, env: Env = global_env) -> Exp:
    if isinstance(ast, Symbol):
        return env.find(ast)[ast]
    elif not isinstance(ast, list):
        return ast
    
    op, *args = ast
    if op == "quote":
        return args[0]
    elif op == "define":
        (symbol, exp) = args
        env[symbol] = eval(exp, env)
    elif op == "if":
        (cond, true_br, false_br) = args
        # eval cond first
        if eval(cond, env):
            return eval(true_br, env)
        else:
            return eval(false_br, env)
    elif op == "set!":
        (symbol, exp) = args
        env.find(symbol)[symbol] = eval(exp, env)
    elif op == "lambda":
        (params, body) = args
        return Procedure(params, body, env)
    else:
        # generic function call
        func = eval(op, env)
        args = [eval(arg, env) for arg in args]
        return func(*args)

if __name__ == "__main__":
    program = """
        (begin 
            (define fib
                (lambda (n)
                    (if (< n 2)
                        1
                        (+ (fib (- n 1)) (fib (- n 2))))))
            (define range
                (lambda (a b)
                    (if (= a b) 
                        (quote ())
                        (cons a (range (+ a 1) b)))))
            (map fib (range 0 25)))
    """
    ast = parse(program)
    print(list(eval(ast)))
