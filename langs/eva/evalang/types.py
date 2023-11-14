from enum import Enum

# type base class
class TypeBase:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
class TypeFunctionBase(TypeBase):
    def __init__(self, name=None, param_types=None, return_type=None):
        self.name = name
        self.param_types = param_types
        self.return_type = return_type

    def __str__(self):
        return f"fn<{self.return_type.value}<{','.join([str(t.value) for t in self.param_types])}>>"
    
    def __eq__(self, other):
        if not isinstance(other, TypeFunctionBase):
            return False
        if len(self.param_types) != len(other.param_types):
            return False
        for i in range(len(self.param_types)):
            if self.param_types[i] != other.param_types[i]:
                return False
        return self.return_type == other.return_type

# type repo
class Type(Enum):
    number = TypeBase("number")
    string = TypeBase("string")
    boolean = TypeBase("boolean")
    function = TypeFunctionBase

    @classmethod
    def from_string(cls, type_str):
        match type_str:
            case "number":
                return Type.number
            case "string":
                return Type.string
            case "boolean":
                return Type.boolean
            case s if s.startswith("fn<"):
                _, return_type, param_types = s.split("<")
                param_types = param_types.replace(">", "").split(",")

                return_ty = cls.from_string(return_type)
                param_tys = [cls.from_string(pty) for pty in param_types]
                return TypeFunctionBase(param_types=param_tys, return_type=return_ty)
            case _:
                raise Exception(f"unknown type: {type_str}")
