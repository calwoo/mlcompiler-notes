from enum import Enum

# type base class
class TypeBase:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
# type repo
class Type(Enum):
    number = TypeBase("number")
    string = TypeBase("string")

    @classmethod
    def from_string(cls, type_str):
        match type_str:
            case "number":
                return Type.number
            case "string":
                return Type.string
            case _:
                raise Exception(f"unknown type: {type_str}")
