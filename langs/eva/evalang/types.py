from enum import Enum
from evalang.typeenvironment import TypeEnvironment

# type base class
class TypeBase:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        if isinstance(other, TypeAliasBase):
            return other == self
        return self.name == other.name
    
class TypeFunctionBase(TypeBase):
    def __init__(self, name=None, param_types=None, return_type=None):
        self.name = f"fn<{return_type.name}<{','.join([str(t.name) for t in param_types])}>>"
        self.param_types = param_types
        self.return_type = return_type
    
    def __eq__(self, other):
        if not isinstance(other, TypeFunctionBase):
            return False
        if len(self.param_types) != len(other.param_types):
            return False
        for i in range(len(self.param_types)):
            if self.param_types[i] != other.param_types[i]:
                return False
        return self.return_type == other.return_type
    
class TypeAliasBase(TypeBase):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return self.parent == other
    
class TypeClassBase(TypeBase):
    def __init__(self, name, superclass=TypeBase("null")):
        self.name = name
        self.superclass = superclass
        parent_env = superclass.env if superclass != TypeBase("null") else None
        self.env = TypeEnvironment(record={}, parent=parent_env)

    def get_field(self, name):
        return self.env.lookup(name)
    
    def __eq__(self, other):
        if self.name == other.name:
            return True
        if isinstance(other, TypeAliasBase):
            return other == self
        if self.superclass != TypeBase("null"):
            return self.superclass == other
        return False
    
class TypeUnionBase(TypeBase):
    def __init__(self, name, option_types):
        self.name = name
        self.option_types = option_types

    def includes_all(self, types):
        if len(types) != len(self.option_types):
            return False
        for type_ in types:
            if self != type_:
                return False
        return True

    def __eq__(self, other):
        if self.name == other.name:
            return True
        if isinstance(other, TypeAliasBase):
            return other == self
        
        # other union
        if isinstance(other, TypeUnionBase):
            return self.includes_all(other.option_types)
        
        match = False
        for opt in self.option_types:
            if opt == other:
                match = True
        return match

# type repo
class Type(Enum):
    number = TypeBase("number")
    string = TypeBase("string")
    boolean = TypeBase("boolean")
    null = TypeBase("null")

    @classmethod
    def function(cls, *args, **kwargs):
        return TypeFunctionBase(*args, **kwargs)
    
    @classmethod
    def alias(cls, *args, **kwargs):
        return TypeAliasBase(*args, **kwargs)
    
    @classmethod
    def classtype(cls, *args, **kwargs):
        return TypeClassBase(*args, **kwargs)
    
    @classmethod
    def union(cls, *args, **kwargs):
        return TypeUnionBase(*args, **kwargs)

    @classmethod
    def from_string(cls, type_str):
        match type_str:
            case "number":
                return Type.number.value
            case "string":
                return Type.string.value
            case "boolean":
                return Type.boolean.value
            case s if s.startswith("fn<"):
                _, return_type, param_types = s.split("<")
                param_types = param_types.replace(">", "").split(",")

                return_ty = cls.from_string(return_type)
                param_tys = [cls.from_string(pty) for pty in param_types]
                return TypeFunctionBase(param_types=param_tys, return_type=return_ty)
            case _:
                if hasattr(Type, type_str):
                    return getattr(Type, type_str)
                # raise Exception(f"unknown type: {type_str}")
                return Type.null.value
