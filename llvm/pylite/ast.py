from llvmlite import ir


class Number:
    def __init__(self, module, builder, value):
        self.value = value
        self.module = module
        self.builder = builder
    
    def eval(self):
        i = ir.Constant(ir.IntType(8), int(self.value))
        return i
    
class BinaryOp:
    def __init__(self, module, builder, left, right):
        self.module = module
        self.builder = builder
        self.left = left
        self.right = right

class Sum(BinaryOp):
    def eval(self):
        i = self.builder.add(self.left.eval(), self.right.eval())
        return i
    
class Sub(BinaryOp):
    def eval(self):
        i = self.builder.sub(self.left.eval(), self.right.eval())
        return i
    
class Print:
    def __init__(self, module, builder, printf_fn, value):
        self.module = module
        self.builder = builder
        self.printf_fn = printf_fn
        self.value = value

    def eval(self):
        val = self.value.eval()

        # add call to printf
        voidptr_type = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf-8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = "internal"
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_type)

        self.builder.call(self.printf_fn, [fmt_arg, val])
