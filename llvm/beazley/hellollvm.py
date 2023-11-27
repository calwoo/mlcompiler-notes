from llvmlite import ir, binding
from ctypes import CFUNCTYPE, c_int


mod = ir.Module("hello")
int_type = ir.IntType(32)
double_type = ir.DoubleType()
void_type = ir.VoidType()

x_var = ir.GlobalVariable(mod, double_type, "x")
x_var.initializer = ir.Constant(double_type, 0.0)

_print_int = ir.Function(
    mod, 
    ir.FunctionType(void_type, [int_type]), 
    name="_print_int"
)

hello_func = ir.Function(mod, ir.FunctionType(int_type, []), name="hello")
block = hello_func.append_basic_block("entry")
builder = ir.IRBuilder(block)

x = builder.alloca(int_type, name="x")
y = builder.alloca(int_type, name="y")
builder.store(ir.Constant(int_type, 4), x)
builder.store(ir.Constant(int_type, 5), y)
r1 = builder.load(x)
r2 = builder.load(y)
r3 = builder.mul(r1, r1)
r4 = builder.mul(r2, r2)
r5 = builder.add(r3, r4)
d = builder.alloca(int_type, name="d")
builder.store(r5, d)
builder.call(_print_int, [builder.load(d)])
builder.ret(ir.Constant(int_type, 42))

# another function
dsquared_func = ir.Function(
    mod, 
    ir.FunctionType(double_type, [double_type, double_type]), 
    name="dsquared"
)
block = dsquared_func.append_basic_block("entry")
builder = ir.IRBuilder(block)

x, y = dsquared_func.args
xsq = builder.fmul(x, x)
ysq = builder.fmul(y, y)
d2 = builder.fadd(xsq, ysq)
builder.ret(d2)

print(mod)

def run_jit(module):
    binding.initialize()
    binding.initialize_native_target()
    binding.initialize_native_asmprinter()

    target = binding.Target.from_default_triple()
    target_machine = target.create_target_machine()
    compiled_mod = binding.parse_assembly(str(module))
    engine = binding.create_mcjit_compiler(compiled_mod, target_machine)

    # look up function
    func_ptr = engine.get_function_address("hello")
    hello_func = CFUNCTYPE(c_int)(func_ptr)

    res = hello_func()
    print(f"hello() returned {res}")

# run_jit(mod)
