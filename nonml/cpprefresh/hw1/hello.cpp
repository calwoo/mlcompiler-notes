#include <iostream>


int main() {
    const char *hello = "hello world!";
    int n;

    std::cin >> n;

    for (int i = 0; i < n; i++) {
        std::cout << hello << std::endl;
    }
    return 0;
}
