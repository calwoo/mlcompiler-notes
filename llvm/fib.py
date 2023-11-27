from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int64


mod = ir.Module(name="fib")

int_type = ir.IntType(64);
int_to_int_fn_type = ir.FunctionType(int_type, [int_type])

# fibonacci function fib: int -> int
fib_fn = ir.Function(mod, int_to_int_fn_type, name="fib")
fib_fn_block = fib_fn.append_basic_block("entry")
builder = ir.IRBuilder(fib_fn_block)

# if n <= 1
(n,) = fib_fn.args
n_lt_1 = builder.icmp_signed(
    cmpop="<=",
    lhs=n,
    rhs=ir.Constant(int_type, 1)
)
# then ret 1
with builder.if_then(n_lt_1):
    builder.ret(ir.Constant(int_type, 1))

# else ret fib(n-1) + fib(n-2)
n_minus_1 = builder.sub(n, ir.Constant(int_type, 1))
n_minus_2 = builder.sub(n, ir.Constant(int_type, 2))
fib_1 = builder.call(fib_fn, [n_minus_1])
fib_2 = builder.call(fib_fn, [n_minus_2])
recurse = builder.add(fib_1, fib_2)
builder.ret(recurse)

print(mod)

# running function
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# Create a target machine representing the host
target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()
# And an execution engine with an empty backing module
backing_mod = llvm.parse_assembly("")
engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

# Compile the LLVM IR string with the given engine.
mod = llvm.parse_assembly(str(mod))
mod.verify()
# Now add the module and make sure it is ready for execution
engine.add_module(mod)
engine.finalize_object()
engine.run_static_constructors()

fib_fn_ptr = engine.get_function_address("fib")
fib_fn_c = CFUNCTYPE(c_int64, c_int64)(fib_fn_ptr)

for n in range(50):
    print(f"fib({n}) = {fib_fn_c(n)}")
