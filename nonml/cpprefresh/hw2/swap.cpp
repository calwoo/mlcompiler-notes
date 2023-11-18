#include <iostream>

void swap(int& a, int&b) {
    int tmp = a;
    a = b;
    b = tmp;
}

int main() {
    int a = 3;
    int b = 4;

    std::cout << a << b << std::endl;
    swap(a, b);
    std::cout << a << b << std::endl;
    return 0;
}
