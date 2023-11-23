#include <string>

#include "./src/EvaLLVM.h"

int main(int argc, char const *argv[]) {
    std::string program = R"(
        (printf "value: %d" 42)
    )";

    EvaLLVM vm;

    vm.exec(program);
    return 0;
}
