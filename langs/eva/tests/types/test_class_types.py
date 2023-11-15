import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


@pytest.mark.parametrize("expr, expected", [
    ("""
    (begin
        (class Point null
            (begin
                (var (x number) 0)
                (var (y number) 0)
     
                (def constructor ((self Point) (x number) (y number)) -> Point
                    (begin
                        (set (prop self x) x)
                        (set (prop self y) y)
                        self))

                (def calc ((self Point)) -> number
                    (+ (prop self x) (prop self y)))))
     
        (var (p Point) (new Point 10 20))
        ((prop p calc) p)
    )
    """, Type.number),
    ("""
    (begin
        (class Point null
            (begin
                (var (x number) 0)
                (var (y number) 0)
     
                (def constructor ((self Point) (x number) (y number)) -> Point
                    (begin
                        (set (prop self x) x)
                        (set (prop self y) y)
                        self))

                (def calc ((self Point)) -> number
                    (+ (prop self x) (prop self y)))))

        (class Point3D Point
            (begin
                (var (z number) 0)
                (def constructor ((self Point3D) (x number) (y number) (z number)) -> Point3D
                    (begin
                        ((prop (super Point3D) constructor) self x y)
                        (set (prop self z) z)
                        self))
    
                (def calc ((self Point3D)) -> number
                    (+ ((prop (super Point3D) calc) self)
                        (prop self z)))))

        (var (p Point3D) (new Point3D 10 20 30))
        ((prop p calc) p)
    )
    """, Type.number),
])
def test_classes(expr, expected):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == expected

