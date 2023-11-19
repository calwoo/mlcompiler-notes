#include <iostream>

using namespace std;

int main()
{
    short number;
    cout << "enter a number :";
    cin >> number;

    cout << "the factorial of " << number << " is ";
    int accumulator = 1;
    for (; number > 0; accumulator *= number--);
    cout << accumulator << ".\n";

    return 0;
}
