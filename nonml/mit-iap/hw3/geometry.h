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

class PointArray
{
private:
    int size;
    Point *points;
    void resize(int size);

public:
    PointArray();
    PointArray(const Point pts[], const int size);
    PointArray(const PointArray& pv);
    ~PointArray();

    void clear();
    int getSize() const { return size; }
    void pushBack(const Point& p);
    void insert(const int pos, const Point& p);
    void remove(const int pos);
    Point* get(const int pos);
    const Point* get(const int pos) const;
};
