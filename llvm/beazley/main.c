#include <stdio.h>

extern int hello();
extern double dsquared(double, double);

int main()
{
    printf("hello() returned %d\n", hello());
    printf("dsquared(3, 4) = %f\n", dsquared(3.0, 4.0));
}
