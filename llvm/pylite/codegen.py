from llvmlite import ir, binding


class CodeGen:
    def __init__(self):
        binding.initialize()
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()

        # initialize module
        self.module = ir.Module(name=__file__)
        main_func = ir.Function(
            self.module,
            ir.FunctionType(ir.VoidType(), []),
            name="main",
        )
        block = main_func.append_basic_block("entry")
        self.builder = ir.IRBuilder(block)

        target = binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        compiled_mod = binding.parse_assembly("")
        self.engine = binding.create_mcjit_compiler(compiled_mod, target_machine)

        # add printf
        voidptr_type = ir.IntType(8).as_pointer()
        printf_func = ir.Function(
            self.module,
            ir.FunctionType(ir.IntType(32), [voidptr_type], var_arg=True),
            name="printf",
        )
        self.printf = printf_func

    def compile(self):
        self.builder.ret_void()

        llvm_ir = str(self.module)
        mod = binding.parse_assembly(llvm_ir)
        mod.verify()

        self.engine.add_module(mod)
        self.engine.finalize_object()
        self.engine.run_static_constructors()
        return mod

    def save_ir(self):
        with open("output.ll", "w") as f:
            f.write(str(self.module))
