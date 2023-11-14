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
