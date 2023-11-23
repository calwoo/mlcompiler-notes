#ifndef EvaLLVM_H
#define EvaLLVM_H

#include <string>
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"

class EvaLLVM {
    public:
        EvaLLVM() { moduleInit(); }
        
        // executes program
        void exec(const std::string& program) {
            // parse program
            // auto ast = parser->parse(program);

            // compile to LLVM-IR
            // compile(ast);

            // print generated code
            module->print(llvm::outs(), nullptr);

            // save module IR to file
            saveModuleToFile("./out.ll");
        }

    private:
        void moduleInit() {
            ctx = std::make_unique<llvm::LLVMContext>();
            module = std::make_unique<llvm::Module>("EvaLLVM", *ctx);
            builder = std::make_unique<llvm::IRBuilder<>>(*ctx);
        }

        void saveModuleToFile(const std::string& fileName) {
            std::error_code errorCode;
            llvm::raw_fd_ostream outLL(fileName, errorCode);
            module->print(outLL, nullptr);
        }

        /**
         * global LLVM context, owns and manages core "global" data of LLVM's
         * core infra, including type and constant unique tables
        */
        std::unique_ptr<llvm::LLVMContext> ctx;

        /**
         * module instance stores all info related to an LLVM module
        */
        std::unique_ptr<llvm::Module> module;

        /**
         * IR builder, provides a uniform API for creating instructions and adding
         * them into basic blocks
        */
        std::unique_ptr<llvm::IRBuilder<>> builder;
};

#endif
