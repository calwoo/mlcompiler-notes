class Environment:
    def __init__(self, record={}, parent=None):
        self.record = record
        self.parent = parent

    def define(self, name, value):
        self.record[name] = value
        return value
    
    def assign(self, name, value):
        if name not in self.record:
            # identifier resolution
            if self.parent is None:
                raise ValueError(f"variable {name} not defined")
            return self.parent.assign(name, value)
        self.record[name] = value
        return value
    
    def lookup(self, name):
        if name not in self.record:
            # identifier resolution
            if self.parent is None:
                raise ValueError(f"variable {name} not defined")
            return self.parent.lookup(name)
        return self.record[name]
