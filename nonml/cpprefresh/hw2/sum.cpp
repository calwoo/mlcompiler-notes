#include <iostream>


// int sum(int a, int b) {
//     return a + b;
// }

double sum(double a, double b) {
    return a + b;
}

// int sum(int a, int b, int c) {
//     return a + b + c;
// }

int sum(int a, int b, int c=0, int d=0) {
    return a + b + c + d;
}

int sum(int nums[], int len) {
    int s = 0;
    for (auto i = 0; i < len; i++) {
        s += nums[i];
    }
    return s;
}

int main() {
    int test = sum(1, 4, 2);
    std::cout << test << std::endl;

    test = sum(1, 4, 2, -2);
    std::cout << test << std::endl;

    int nums[5] = {1, 3, 2, 5, -1};
    test = sum(nums, 5);
    std::cout << test << std::endl;
    return 0;
}
