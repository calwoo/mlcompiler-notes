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
        # math ops
        if self.is_binary(exp):
            return self.binary(exp, env)
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

        if self.is_variable_name(exp):
            return env.lookup(exp)
        
        raise ValueError(f"unknown type for: {exp}")
    
    def create_global(self):
        return TypeEnvironment(record={
            "VERSION": Type.string
        })
    
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

    def check_arity(self, exp, arity):
        if len(exp) - 1 != arity:
            raise Exception(f"operator {exp[0]} expected {arity} ops, got {len(exp) - 1}")
        
    def get_operand_types_for_operator(self, op):
        match op:
            case '+':
                return [Type.string, Type.number]
            case '*':
                return [Type.number]
            case '-':
                return [Type.number]
            case '/':
                return [Type.number]
            case _:
                raise Exception(f"unknown op: {op}")
        
    def is_number(self, exp):
        return isinstance(exp, int) or isinstance(exp, float)

    def is_string(self, exp):
        return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'

    def is_binary(self, exp):
        ops = re.compile(r'^[\+\-\*\/]$')
        return bool(ops.match(exp[0]))
    
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
