import pytest
from evalang import Eva
from evalang.parse import parse


@pytest.mark.parametrize("expr, expected", [
    ("""
    (begin
        (class Point null
            (begin
                (def constructor (this x y)
                    (begin
                        (set (prop this x) x)
                        (set (prop this y) y)))
                (def calc (this)
                    (+ (prop this x) (prop this y)))))

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
                (def constructor (this x y)
                    (begin
                        (set (prop this x) x)
                        (set (prop this y) y)))
                (def calc (this)
                    (+ (prop this x) (prop this y)))))

        (class Point3D Point
            (begin
                (def constructor (this x y z)
                    (begin
                        ((prop (super Point3D) constructor) this x y)
                        (set (prop this z) z)))
                (def calc (this)
                    (+ ((prop (super Point3D) calc) this)
                       (prop this z)))))

        (var p (new Point3D 10 20 30))
        ((prop p calc) p)
    )
    """, 60)
])
def test_class_inheritance(expr, expected):
    eva = Eva()
    assert eva.eval(parse(expr)) == expected