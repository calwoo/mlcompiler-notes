import re
from evalang.environment import Environment


class Eva:
    def __init__(self, globalenv: Environment = None):
        self.globalenv = globalenv
        if globalenv is None:
            self.globalenv = Environment(record={
                "null": None,
                "true": True,
                "false": False,
                "VERSION": "0.1"
            })

    def eval(self, exp, env=None):
        if env is None:
            env = self.globalenv

        """self-evaluating expressions"""
        if is_number(exp):
            return exp
        if is_string(exp):
            return exp[1:-1]
        
        """math operations"""
        if exp[0] == '+':
            return self.eval(exp[1], env) + self.eval(exp[2], env)
        if exp[0] == '*':
            return self.eval(exp[1], env) * self.eval(exp[2], env)
        
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
        if is_variable_name(exp):
            return env.lookup(exp)

        raise NotImplementedError(exp)
    
    def eval_block(self, block, env):
        _, *expressions = block
        result = None
        for exp in expressions:
            result = self.eval(exp, env)
        return result

def is_number(exp):
    return isinstance(exp, int) or isinstance(exp, float)

def is_string(exp):
    # strings have to be delimited by double quotes ""
    return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'

def is_variable_name(exp):
    valid_regex = re.compile(r'^[a-zA-Z][a-zA-Z0-9)]*')
    return isinstance(exp, str) and bool(valid_regex.match(exp))
