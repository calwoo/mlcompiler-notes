import re
from evalang.environment import Environment
from evalang.transformer import ASTTransformer


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
    "print": lambda *args: print(args)
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
            (_, ref, value) = exp
            
            if ref[0] == "prop":
                (_, instance, attribute) = ref
                instance_env = self.eval(instance, env)
                return instance_env.define(attribute, self.eval(value, env))

            return env.assign(ref, self.eval(value, env))
        
        """variable access"""
        if self.is_variable_name(exp):
            return env.lookup(exp)
        
        """syntactic sugar inc"""
        if exp[0] == "++":
            desugared_exp = ASTTransformer.transform_inc_to_set(exp)
            return self.eval(desugared_exp, env)
        
        """syntactic sugar inc"""
        if exp[0] == "+=":
            desugared_exp = ASTTransformer.transform_incassign_to_set(exp)
            return self.eval(desugared_exp, env)
        
        """syntactic sugar dec"""
        if exp[0] == "--":
            desugared_exp = ASTTransformer.transform_dec_to_set(exp)
            return self.eval(desugared_exp, env)
        
        """syntactic sugar dec"""
        if exp[0] == "-=":
            desugared_exp = ASTTransformer.transform_decassign_to_set(exp)
            return self.eval(desugared_exp, env)
        
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
        
        """for-expression"""
        if exp[0] == "for":
            desugared_exp = ASTTransformer.transform_for_to_while(exp)
            return self.eval(desugared_exp, env)
        
        """function declaration
        
        (def square (x) (* x x))
        sugar for: (var square (lambda (x) (* x x)))
        """
        if exp[0] == "def":
            # (_, fn_name, fn_params, fn_body) = exp
            # fn = {
            #     "name": fn_name,
            #     "params": fn_params,
            #     "body": fn_body,
            #     "closure": env,
            # }
            # return env.define(fn_name, fn)
            desugared_exp = ASTTransformer.transform_def_to_var_lambda(exp)
            return self.eval(desugared_exp, env)
        
        """switch statement"""
        if exp[0] == "switch":
            if_exp = ASTTransformer.transform_switch_to_if(exp)
            return self.eval(if_exp, env)
        
        """lambda declaration"""
        if exp[0] == "lambda":
            (_, lam_params, lam_body) = exp
            return {
                "params": lam_params,
                "body": lam_body,
                "closure": env,
            }
        
        """class declaration"""
        if exp[0] == "class":
            (_, name, parent, body) = exp
            parent_env = self.eval(parent, env) or env
            class_env = Environment(record={}, parent=parent_env)
            self.eval_block(body, class_env)
            return env.define(name, class_env)
        
        """new instance instantiation"""
        if exp[0] == "new":
            (_, class_name, *class_args) = exp
            class_env = self.eval(class_name, env)
            # instance of a class is an environment
            instance_env = Environment(record={}, parent=class_env)
            self.call_user_defined_function(
                class_env.lookup("constructor"),
                [instance_env, *class_args]
            )
            return instance_env
        
        """instance property access"""
        if exp[0] == "prop":
            (_, instance, attribute) = exp
            instance_env = self.eval(instance, env)
            return instance_env.lookup(attribute)
        
        """function calls"""
        if isinstance(exp, list):
            fn_name, *args = exp
            fn = self.eval(fn_name, env)
            # eval args first
            args_evaled = [self.eval(arg, env) for arg in args]

            # native function
            if callable(fn):
                return fn(*args_evaled)
            
            # user-defined function
            return self.call_user_defined_function(fn, args_evaled)

        raise NotImplementedError(exp)
    
    def call_user_defined_function(self, fn, args):
        activation_record = {}
        for i, arg in enumerate(args):
            activation_record[fn["params"][i]] = arg
        activation_env = Environment(record=activation_record, parent=fn["closure"])
        return self.eval(fn["body"], activation_env)
    
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
        valid_regex = re.compile(r'^[+\-*.<>=a-zA-Z][a-zA-Z0-9)]*')
        return isinstance(exp, str) and bool(valid_regex.match(exp))
