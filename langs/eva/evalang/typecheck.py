from evalang.types import Type


class EvaTC:
    """
    static type-checker for eva
    """

    def tc(self, exp):
        if self.is_number(exp):
            return Type.number
        if self.is_string(exp):
            return Type.string
        
        raise ValueError(f"unknown type for: {exp}")
        
    def is_number(self, exp):
        return isinstance(exp, int) or isinstance(exp, float)

    def is_string(self, exp):
        return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'
