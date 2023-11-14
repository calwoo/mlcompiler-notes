class TypeEnvironment:
    def __init__(self, record={}, parent=None):
        self.record = record
        self.parent = parent

    def define(self, name, type_):
        self.record[name] = type_
        return type_

    def lookup(self, name):
        if name not in self.record:
            raise Exception(f"variable {name} not found")
        return self.record[name]
