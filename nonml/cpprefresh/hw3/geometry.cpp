#include <iostream>
#include "geometry.h"

Point::Point(int u=0, int v=0)
{
    x = u;
    y = v;
}

int Point::getX() const
{
    return x;
}

int Point::getY() const
{
    return y;
}

void Point::setX(const int new_x)
{
    x = new_x;
}

void Point::setY(const int new_y)
{
    y = new_y;
}

int main()
{
    Point origin = Point();
    Point p = Point(2, 3);

    std::cout << origin.getX() << " " << origin.getY() << std::endl;
    std::cout << p.getX() << " " << p.getY() << std::endl;

    p.setX(5);
    p.setY(-2);
    std::cout << p.getX() << " " << p.getY() << std::endl;

    return 0;
}
