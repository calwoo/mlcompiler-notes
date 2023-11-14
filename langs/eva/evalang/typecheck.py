import re
from evalang.types import Type
from evalang.typeenvironment import TypeEnvironment


class EvaTC:
    """
    static type-checker for eva
    """

    def __init__(self):
        self.globalenv = self.create_global()

    def tc(self, exp, env=None):
        if env is None:
            env = self.globalenv

        if self.is_number(exp):
            return Type.number
        if self.is_string(exp):
            return Type.string
        if self.is_boolean(exp):
            return Type.boolean
        # math ops
        if self.is_binary(exp):
            return self.binary(exp, env)
        # bool ops
        if self.is_boolean_binary(exp):
            return self.boolean_binary(exp, env)
        # var declarations and access
        if exp[0] == "var":
            (_, name, value) = exp
            value_type = self.tc(value, env)
            if isinstance(name, list):
                # if we declare type explicitly, check match
                (var_name, type_str) = name
                expected_type = Type.from_string(type_str)
                self.expect(value_type, expected_type, value, exp)
                return env.define(var_name, expected_type)
            return env.define(name, value_type)
        
        if exp[0] == "set":
            (_, name, value) = exp
            # just verify that new value is same type as var
            var_type = self.tc(name, env)
            val_type = self.tc(value, env)
            self.expect(val_type, var_type, value, exp)
            return val_type

        if self.is_variable_name(exp):
            return env.lookup(exp)
        
        # conditionals
        if exp[0] == "if":
            (_, cond, t_br, f_br) = exp
            cond_type = self.tc(cond, env)
            self.expect(cond_type, Type.boolean, cond, exp)

            t_br_type = self.tc(t_br, env)
            f_br_type = self.tc(f_br, env)
            return self.expect(f_br_type, t_br_type, exp, exp)
        
        if exp[0] == "while":
            (_, cond, body) = exp
            cond_type = self.tc(cond, env)
            self.expect(cond_type, Type.boolean, cond, exp)
            return self.tc(body, env)
        
        # function declarations
        if exp[0] == "def":
            (_, name, params, _, return_typestr, body) = exp
            fn_type = self.function(params, return_typestr, body, env)
            env.define(name, fn_type)
            return fn_type
        
        # block
        if exp[0] == "begin":
            block_env = TypeEnvironment(record={}, parent=env)
            return self.block(exp, block_env)   
        
        # function calls
        if isinstance(exp, list):
            fn_name, *args = exp
            fn_type = self.tc(fn_name, env)
            # typecheck args
            arg_types = [self.tc(arg, env) for arg in args]
            if len(fn_type.param_types) != len(arg_types):
                raise Exception(f"not enough args: need {len(fn_type.param_types)}")
            
            for arg_t, param_t in zip(arg_types, fn_type.param_types):
                if arg_t != param_t:
                    raise Exception(f"mismatched params, need {param_t}, got {arg_t}")
            return fn_type.return_type
        
        raise ValueError(f"unknown type for: {exp}")
    
    def create_global(self):
        return TypeEnvironment(record={
            "VERSION": Type.string
        })
    
    def block(self, block, env):
        _, *expressions = block
        result = None
        for exp in expressions:
            result = self.tc(exp, env)
        return result
    
    def function(self, params, return_typestr, body, env):
        return_type = Type.from_string(return_typestr)
        # function bodies create new scope
        params_record = {}
        param_types = []
        for name, typestr in params:
            param_type = Type.from_string(typestr)
            params_record[name] = param_type
            param_types.append(param_type)
        
        fn_env = TypeEnvironment(record=params_record, parent=env)
        actual_return_type = self.tc(body, fn_env)

        if return_type != actual_return_type:
            raise Exception(f"expected function to return {return_type}, got {actual_return_type}")
        return Type.function.value(param_types=param_types, return_type=return_type)
    
    def binary(self, exp, env):
        self.check_arity(exp, 2)
        # check each entry
        (op, e1, e2) = exp
        t1 = self.tc(e1, env)
        t2 = self.tc(e2, env)

        allowed_types = self.get_operand_types_for_operator(op)
        self.expect_operator_type(t1, allowed_types, exp)
        self.expect_operator_type(t2, allowed_types, exp)
        return self.expect(t2, t1, e2, exp)
    
    def boolean_binary(self, exp, env):
        self.check_arity(exp, 2)
        (op, e1, e2) = exp
        t1 = self.tc(e1, env)
        t2 = self.tc(e2, env)

        allowed_types = self.get_operand_types_for_operator(op)
        self.expect_operator_type(t1, allowed_types, exp)
        self.expect_operator_type(t2, allowed_types, exp)
        self.expect(t2, t1, e2, exp)
        return Type.boolean

    def check_arity(self, exp, arity):
        if len(exp) - 1 != arity:
            raise Exception(f"operator {exp[0]} expected {arity} ops, got {len(exp) - 1}")
        
    def get_operand_types_for_operator(self, op):
        match op:
            case '+': return [Type.string, Type.number]
            case '*': return [Type.number]
            case '-': return [Type.number]
            case '/': return [Type.number]
            case '>': return [Type.number]
            case '<': return [Type.number]
            case ">=": return [Type.number]
            case "<=": return [Type.number]
            case "==": return [Type.number, Type.string]
            case "!=": return [Type.number, Type.string]
            case _:
                raise Exception(f"unknown op: {op}")
        
    def is_number(self, exp):
        return isinstance(exp, int) or isinstance(exp, float)

    def is_string(self, exp):
        return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'

    def is_boolean(self, exp):
        return isinstance(exp, bool) or exp in ["true", "false"]

    def is_binary(self, exp):
        ops = re.compile(r'^[\+\-\*\/]$')
        return bool(ops.match(exp[0]))
    
    def is_boolean_binary(self, exp):
        return exp[0] in [">", "<", ">=", "<=", "==", "!="]
    
    def is_variable_name(self, exp):
        reg = re.compile(r'^[\+\-\*\/<>=a-zA-Z0-9_:]+$')
        return isinstance(exp, str) and bool(reg.match(exp))
    
    def expect(self, actual_type, expected_type, value, exp):
        if actual_type != expected_type:
            self.type_error(actual_type, expected_type, value, exp)
        return actual_type
    
    def expect_operator_type(self, _type, allowed_types, exp):
        if _type not in allowed_types:
            raise Exception(f"unexpected type {_type} in {exp}, allowed types are {allowed_types}")
    
    def type_error(self, actual_type, expected_type, value, exp):
        raise Exception(f"expected {expected_type} type for {value} in {exp}, got {actual_type}")
