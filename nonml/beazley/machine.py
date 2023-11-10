import struct


class Function:
    def __init__(self, nparams, returns, code):
        self.nparams = nparams
        self.returns = returns
        self.code = code

class Machine:
    def __init__(self, functions, memsize=65536):
        self.functions = functions # function table
        self.stack = []
        self.memory = bytearray(memsize)

    def load(self, addr):
        return struct.unpack('<d', self.memory[addr:addr+8])[0]

    def store(self, addr, val):
        self.memory[addr:addr+8] = struct.pack('<d', val)

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()
    
    def call(self, func, *args):
        locals = dict(enumerate(args))
        self.execute(func.code, locals)
        if func.returns:
            return self.pop()
    
    def execute(self, instructions, locals):
        for op, *args in instructions:
            print(op, args, self.stack)
            if op == "const":
                self.push(args[0])
            elif op == "add":
                right = self.pop()
                left = self.pop()
                self.push(left + right)
            elif op == "mul":
                right = self.pop()
                left = self.pop()
                print(left, right)
                self.push(left * right)
            elif op == "load":
                addr = self.pop()
                self.push(self.load(addr))
            elif op == "store":
                val = self.pop()
                addr = self.pop()
                self.store(addr, val)
            elif op == "local.get":
                self.push(locals[args[0]])
            elif op == "local.set":
                locals[args[0]] = self.pop()
            elif op == "call":
                func = self.functions[args[0]]
                fargs = reversed([self.pop() for _ in range(func.nparams)])
                result = self.call(func, *fargs)
                if func.returns:
                    self.push(result)
            elif op == "br":
                raise Break(args[0])
            elif op == "br_if":
                if self.pop():
                    raise Break(args[0])
            elif op == "block":   # ('block', [ instructions ])
                try:
                    self.execute(args[0], locals)
                except Break as b:
                    if b.level > 0:
                        b.level -= 1
                        raise b
            # if (test) { consequence } else { alternative }

            # ("block", [
            #     ("block": [
            #         test
            #         ("br_if", 0)  # goto 0
            #         atlernative,
            #         ("br", 1)     # goto 1
            #     ])  # label 0
            # ])  # label 1

            elif op == "loop":
                while True:
                    try:
                        self.execute(args[0])
                        break
                    except Break as b:
                        if b.level > 0:
                            b.level -= 1
                            raise
            else:
                raise RuntimeError(f"bad op {op}")
            
class Break(Exception):
    def __init__(self, level):
        self.level = level
    
def example():
    # def update_position(x, v, dt):
    #     return x + v * dt
    update_position = Function(nparams=3, returns=True, code=[
        ("local.get", 0), # x
        ("local.get", 1), # v
        ("local.get", 2), # dt
        ("mul",),
        ("add",),
    ])

    functions = [update_position]
    # x = 2
    # v = 3
    # x = x + v * 0.1
    x_addr = 22
    v_addr = 42

    code = [
        ("const", x_addr),
        ("const", x_addr),
        ("load",),
        ("const", v_addr),
        ("load",),
        ("const", 0.1),
        ("call", 0), # update_position
        ("store",)
    ]

    m = Machine(functions)
    m.store(x_addr, 2.0)
    m.store(v_addr, 3.0)
    m.execute(code, None)
    print(f"result: {m.load(x_addr)}")

if __name__ == "__main__":
    example()
