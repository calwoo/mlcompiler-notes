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
            (_, ref, value) = exp
            if ref[0] == "prop":
                (_, instance, prop_name) = ref
                instance_type = self.tc(instance, env)

                value_type = self.tc(value, env)
                prop_type = instance_type.get_field(prop_name)
                return self.expect(value_type, prop_type, value, exp)

            # just verify that new value is same type as var
            var_type = self.tc(ref, env)
            val_type = self.tc(value, env)
            return self.expect(val_type, var_type, value, exp)

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
            fn_type = self.function(name, params, return_typestr, body, env)
            env.define(name, fn_type)
            return fn_type
        
        # lambda
        if exp[0] == "lambda":
            (_, params, _, return_typestr, body) = exp
            fn_type = self.function(None, params, return_typestr, body, env)
            return fn_type
        
        # typedefs
        if exp[0] == "type":
            (_, name, base) = exp
            if name in Type._member_names_:
                raise Exception(f"type {name} already is defined")
            if base not in Type._member_names_:
                raise Exception(f"type {base} not defined")
            typedef = Type.alias(name, Type.from_string(base))
            setattr(Type, name, typedef)
            return typedef
        
        # class typedef
        if exp[0] == "class":
            (_, name, superclass_name, body) = exp
            superclass = Type.from_string(superclass_name)
            class_type = Type.classtype(name=name, superclass=superclass)
            if class_type.env.parent is None:
                class_type.env.parent = env
            setattr(Type, name, class_type)
            env.define(name, class_type)
            # eval body
            self.tc_block(body, class_type.env)
            return class_type
        
        # class instantiation
        if exp[0] == "new":
            (_, classname, *args) = exp
            class_type = Type.from_string(classname)
            if class_type == Type.from_string("null"):
                raise Exception("unknown class")
            
            arg_types = [self.tc(arg, env) for arg in args]
            return self.check_function_call(
                class_type.get_field("constructor"),
                [class_type, *arg_types],
                env,
                exp,
            )
        
        # super (inheritance)
        if exp[0] == "super":
            (_, classname) = exp
            class_type = Type.from_string(classname)
            if class_type is None:
                raise Exception(f"unknown class {classname}")
            return class_type.superclass
        
        if exp[0] == "prop":
            (_, instance, attr) = exp
            instance_type = self.tc(instance, env)
            return instance_type.get_field(attr)

        # block
        if exp[0] == "begin":
            block_env = TypeEnvironment(record={}, parent=env)
            result = self.block(exp, block_env)
            return result
        
        # function calls
        if isinstance(exp, list):
            fn_name, *args = exp
            fn_type = self.tc(fn_name, env)
            # typecheck args
            arg_types = [self.tc(arg, env) for arg in args]
            return self.check_function_call(fn_type, arg_types, env, exp)
        
        raise ValueError(f"unknown type for: {exp}")
    
    def tc_block(self, block, env):
        result = self.block(block, env)
        return result
    
    def check_function_call(self, fn_type, arg_types, env, exp):
        if len(fn_type.param_types) != len(arg_types):
            raise Exception(f"not enough args: need {len(fn_type.param_types)}")
        
        for arg_t, param_t in zip(arg_types, fn_type.param_types):
            if arg_t != param_t:
                raise Exception(f"mismatched params, need {param_t}, got {arg_t}")
        return fn_type.return_type
    
    def create_global(self):
        return TypeEnvironment(record={
            "VERSION": Type.string,
            "sum": Type.from_string("fn<number<number,number>>"),
            "square": Type.from_string("fn<number<number>>")
        })
    
    def block(self, block, env):
        _, *expressions = block
        result = None
        for exp in expressions:
            result = self.tc(exp, env)
        return result
    
    def function(self, name, params, return_typestr, body, env):
        return_type = Type.from_string(return_typestr)
        # function bodies create new scope
        params_record = {}
        param_types = []
        for pname, typestr in params:
            param_type = Type.from_string(typestr)
            params_record[pname] = param_type
            param_types.append(param_type)
        fn_env = TypeEnvironment(record=params_record, parent=env)

        if name is not None:
            # to allow for recursive function type checking
            fn_env.define(name, Type.function(param_types=param_types, return_type=return_type))
        actual_return_type = self.tc(body, fn_env)

        if return_type != actual_return_type:
            raise Exception(f"expected function to return {return_type}, got {actual_return_type}")
        return Type.function(param_types=param_types, return_type=return_type)
    
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
        if isinstance(exp, list) and isinstance(exp[0], list):
            return False
        ops = re.compile(r'^[\+\-\*\/]$')
        return bool(ops.match(exp[0]))
    
    def is_boolean_binary(self, exp):
        if isinstance(exp, list) and isinstance(exp[0], list):
            return False
        return exp[0] in [">", "<", ">=", "<=", "==", "!="]
    
    def is_variable_name(self, exp):
        if isinstance(exp, list) and isinstance(exp[0], list):
            return False
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
