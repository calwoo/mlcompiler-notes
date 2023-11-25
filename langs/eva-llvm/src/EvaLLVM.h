#ifndef EvaLLVM_H
#define EvaLLVM_H

#include <string>
#include <regex>
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Verifier.h"

#include "./parser/EvaParser.h"
using namespace syntax;

class EvaLLVM {
    public:
        EvaLLVM() : parser(std::make_unique<EvaParser>()) { 
            moduleInit();
            setupExternFunctions();
        }
        
        // executes program
        void exec(const std::string& program) {
            // parse program
            auto ast = parser->parse(program);

            // compile to LLVM-IR
            compile(ast);

            // print generated code
            module->print(llvm::outs(), nullptr);
            std::cout << "\n";

            // save module IR to file
            saveModuleToFile("./out.ll");
        }

    private:
        void moduleInit() {
            ctx = std::make_unique<llvm::LLVMContext>();
            module = std::make_unique<llvm::Module>("EvaLLVM", *ctx);
            builder = std::make_unique<llvm::IRBuilder<>>(*ctx);
        }

        void compile(const Exp& ast) {
            // create main function
            fn = createFunction(
                "main", 
                llvm::FunctionType::get(builder->getInt32Ty(), false)
            );

            // compile main body
            gen(ast);

            builder->CreateRet(builder->getInt32(0));
        }

        /**
         * main compile loop
        */
        llvm::Value* gen(const Exp& exp) {
            switch (exp.type) {
                case ExpType::NUMBER:
                    return builder->getInt32(exp.number);
                case ExpType::STRING: {
                    // unescape special chars
                    auto re = std::regex("\\\\n");
                    auto str = std::regex_replace(exp.string, re, "\n");

                    return builder->CreateGlobalStringPtr(str);
                }
                case ExpType::SYMBOL:
                    // TODO
                    return builder->getInt32(0);
                case ExpType::LIST:
                    auto tag = exp.list[0];
                    
                    if (tag.type == ExpType::SYMBOL) {
                        auto op = tag.string;

                        if (op == "printf") {
                            auto printfFn = module->getFunction("printf");
                            std::vector<llvm::Value*> args{};

                            for (auto i = 1; i < exp.list.size(); i++) {
                                args.push_back(gen(exp.list[i]));
                            }

                            return builder->CreateCall(printfFn, args);
                        }
                    }
            }

            return builder->getInt32(0);
        }

        /**
         * define external functions (from libc++)
        */
        void setupExternFunctions() {
            // i8* to substitute for char*, void*, etc
            auto bytePtrTy = builder->getInt8Ty()->getPointerTo();

            // int printf(const char* format, ...)
            module->getOrInsertFunction("printf", 
                llvm::FunctionType::get(
                    /* return type */ builder->getInt32Ty(),
                    /* format arg */ bytePtrTy,
                    /* vararg */ true));
        }

        llvm::Function* createFunction(const std::string& fnName,
                                       llvm::FunctionType* fnType) {
            // function prototype might already exist
            auto fn = module->getFunction(fnName);
            
            if (fn == nullptr) {
                // if null, allocate
                fn = createFunctionProto(fnName, fnType);
            }

            createFunctionBlock(fn);
            return fn;
        }

        llvm::Function* createFunctionProto(const std::string& fnName,
                                            llvm::FunctionType* fnType) {
            auto fn = llvm::Function::Create(fnType, llvm::Function::ExternalLinkage, 
                                             fnName, *module);
            verifyFunction(*fn);
            return fn;
        }

        void createFunctionBlock(llvm::Function* fn) {
            auto entry = createBB("entry", fn);
            builder->SetInsertPoint(entry);
        }

        llvm::BasicBlock* createBB(std::string name, llvm::Function* fn = nullptr) {
            return llvm::BasicBlock::Create(*ctx, name, fn);
        }

        void saveModuleToFile(const std::string& fileName) {
            std::error_code errorCode;
            llvm::raw_fd_ostream outLL(fileName, errorCode);
            module->print(outLL, nullptr);
        }

        /**
         * parser
        */
        std::unique_ptr<EvaParser> parser;

        /**
         * current function
        */
        llvm::Function* fn;

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
