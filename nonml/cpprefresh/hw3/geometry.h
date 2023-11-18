class Point
{
private:
    int x;
    int y;

public:
    Point(int x, int y);
    int getX() const;
    int getY() const;
    void setX(const int new_x);
    void setY(const int new_y);
};
