#include <iostream>

class Point
{
private:
    int x, y;

public:
    Point(int u, int v) : x(u), y(v) {}
    int getX() { return x; }
    int getY() { return y; }
    void doubleVal()
    {
        x *= 2;
        y *= 2;
    }
};

int main()
{
    // Point myPoint(5, 3);
    // myPoint.doubleVal();
    // std::cout << myPoint.getX() << " " << myPoint.getY() << "\n";

    Point *p = new Point(5, 3);
    std::cout << p->getX() << " " << p->getY() << std::endl;
    return 0;
}
