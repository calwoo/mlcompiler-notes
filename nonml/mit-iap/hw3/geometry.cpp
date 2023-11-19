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

PointArray::PointArray()
{
    size = 0;
    points = new Point[0];
}

PointArray::PointArray(const Point ppts[], const int ssize)
{
    size = ssize;
    points = new Point[ssize];
    for (int i = 0; i < ssize; i++) {
        points[i] = ppts[i];
    }
}

PointArray::PointArray(const PointArray& pvref)
{
    size = pvref.size;
    points = new Point[size];
    for (int i = 0; i < size; i++) {
        points[i] = pvref.points[i];
    }
}

PointArray::~PointArray()
{
    delete [] points;
}

void PointArray::resize(int new_size)
{
    Point* new_pts = new Point[new_size];
    int min_size = (new_size > size ? size : new_size);
    for (int i = 0; i < min_size; i++) {
        new_pts[i] = points[i];
    }
    delete [] points;
    size = new_size;
    points = new_pts;
}

void PointArray::clear()
{
    resize(0);
}

void PointArray::pushBack(const Point& p)
{
    resize(size + 1);
    points[size - 1] = p;
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
