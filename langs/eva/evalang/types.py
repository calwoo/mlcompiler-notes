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
