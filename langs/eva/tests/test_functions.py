import pytest
from evalang import Eva
from evalang.parse import parse


@pytest.mark.parametrize("expr, expected", [
    ("""
    (begin
        (def square (x)
            (* x x))
        (square 2)
    )
    """, 4),
    ("""
    (begin
        (def calc (x y)
            (begin
                (var z 30)
                (+ (* x y) z)
            ))
        (calc 10 20)
    )
    """, 230),
    ("""
    (begin
        (var value 100)
        (def calc (x y)
            (begin
                (var z 30)

                (def inner (foo)
                    (+ (+ foo z) value))
                inner
            ))

        (var fn (calc 10 20))
        (fn 30)
    )
    """, 160)
])
def test_define_funcs(expr, expected):
    eva = Eva()
    assert eva.eval(parse(expr)) == expected

@pytest.mark.parametrize("expr, expected", [
    ("""
    (begin
        (def onClick (callback)
            (begin
                (var x 10)
                (var y 20)
                (callback (+ x y))))
    
        (onClick (lambda (data) (* data 10)))
    )
    """, 300),
    ("""
        ((lambda x (* x x)) 2)
    """, 4),
    ("""
    (begin
        (var square (lambda x (* x x)))
        (square 2)
    )
    """, 4)
])
def test_define_lambda(expr, expected):
    eva = Eva()
    assert eva.eval(parse(expr)) == expected

@pytest.mark.parametrize("expr, expected", [
    ("""
    (begin
        (def factorial (x)
            (if (= x 1)
                1
                (* x (factorial (- x 1)))))
        (factorial 5)
    )
    """, 120),
])
def test_recursive_func(expr, expected):
    eva = Eva()
    assert eva.eval(parse(expr)) == expected
