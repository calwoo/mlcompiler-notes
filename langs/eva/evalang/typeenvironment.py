from pprint import pformat, pprint


class TypeEnvironment:
    def __init__(self, record={}, parent=None):
        self.record = record
        self.parent = parent

    def __str__(self):
        return pformat(self.get_envs())
    
    def get_envs(self):
        env = [{k: str(v) for k, v in self.record.items()}]
        if self.parent is not None:
            env.extend(self.parent.get_envs())
        return env

    def define(self, name, type_):
        self.record[name] = type_
        return type_

    def lookup(self, name):
        if name not in self.record:
            # identifier resolution
            if self.parent is None:
                raise Exception(f"variable {name} not found")
            return self.parent.lookup(name)
        return self.record[name]
