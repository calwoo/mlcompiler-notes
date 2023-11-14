import re
from evalang.environment import Environment


# default global env
globalenv = Environment({
    "null": None,
    "true": True,
    "false": False,
    "VERSION": "0.1",

    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y,
    "-": lambda x, y=None: x - y if y is not None else -x,
    "/": lambda x, y: x / y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    "=": lambda x, y: x == y,
})


class Eva:
    def __init__(self, globalenv: Environment = globalenv):
        self.globalenv = globalenv

    def eval(self, exp, env=None):
        if env is None:
            env = self.globalenv

        """self-evaluating expressions"""
        if self.is_number(exp):
            return exp
        if self.is_string(exp):
            return exp[1:-1]
        
        """block"""
        if exp[0] == "begin":
            # create new block-scoped env
            block_env = Environment(record={}, parent=env)
            return self.eval_block(exp, block_env)
        
        """variable declaration"""
        if exp[0] == "var":
            (_, name, value) = exp
            return env.define(name, self.eval(value, env))
        
        """variable update"""
        if exp[0] == "set":
            (_, name, value) = exp
            return env.assign(name, self.eval(value, env))
        
        """variable access"""
        if self.is_variable_name(exp):
            return env.lookup(exp)
        
        """if-expression"""
        if exp[0] == "if":
            (_, cond, t_br, f_br) = exp
            if self.eval(cond, env):
                return self.eval(t_br, env)
            else:
                return self.eval(f_br, env)
            
        """while-expression"""
        if exp[0] == "while":
            (_, cond, body) = exp
            result = None
            while self.eval(cond, env):
                result = self.eval(body, env)
            return result
        
        """function calls"""
        if isinstance(exp, list):
            fn_name, *args = exp
            fn = env.lookup(fn_name)
            # eval args first
            args_evaled = [self.eval(arg, env) for arg in args]
            return fn(*args_evaled)

        raise NotImplementedError(exp)
    
    def eval_block(self, block, env):
        _, *expressions = block
        result = None
        for exp in expressions:
            result = self.eval(exp, env)
        return result

    def is_number(self, exp):
        return isinstance(exp, int) or isinstance(exp, float)

    def is_string(self, exp):
        # strings have to be delimited by double quotes ""
        return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'

    def is_variable_name(self, exp):
        valid_regex = re.compile(r'^[a-zA-Z][a-zA-Z0-9)]*')
        return isinstance(exp, str) and bool(valid_regex.match(exp))
