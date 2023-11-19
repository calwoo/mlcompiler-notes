#include <iostream>

int main() {
    int size;
    std::cin >> size;

    int *nums = new int[size];
    for (int i = 0; i < size; ++i)
    {
        std::cin >> nums[i];
    }

    delete nums;
    return 0;
}