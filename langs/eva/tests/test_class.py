import pytest
from evalang import Eva
from evalang.parse import parse


@pytest.mark.parametrize("expr, expected", [
    ("""
    (begin
        (class Point null
            (begin
                (def constructor (self x y)
                    (begin
                        (set (prop self x) x)
                        (set (prop self y) y)))
                (def calc (self)
                    (+ (prop self x) (prop self y)))))

        (var p (new Point 10 20))
        ((prop p calc) p)
    )
    """, 30)
])
def test_classes(expr, expected):
    eva = Eva()
    assert eva.eval(parse(expr)) == expected

@pytest.mark.parametrize("expr, expected", [
    ("""
    (begin
        (class Point null
            (begin
                (def constructor (self x y)
                    (begin
                        (set (prop self x) x)
                        (set (prop self y) y)))
                (def calc (self)
                    (+ (prop self x) (prop self y)))))

        (class Point3D Point
            (begin
                (def constructor (self x y z)
                    (begin
                        ((prop (super Point3D) constructor) self x y)
                        (set (prop self z) z)))
                (def calc (self)
                    (+ ((prop (super Point3D) calc) self)
                       (prop self z)))))

        (var p (new Point3D 10 20 30))
        ((prop p calc) p)
    )
    """, 60)
])
def test_class_inheritance(expr, expected):
    eva = Eva()
    assert eva.eval(parse(expr)) == expected