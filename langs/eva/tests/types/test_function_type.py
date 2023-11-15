import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


def test_function_from_string():
    t = Type.from_string("fn<number<number,string>>")
    assert t == Type.function(param_types=[Type.number, Type.string], return_type=Type.number)

@pytest.mark.parametrize("expr", [
    """
    (begin
        (def square ((x number)) -> number (* x x))
        (square 3))
    """,
    """
    (begin
        (def calc ((x number) (y number)) -> number
            (begin
                (var z 30)
                (+ (* x y) z)
            ))
        
        (calc 10 20))
    """
])
def test_basic_functions(expr):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number

@pytest.mark.parametrize("expr", [
    "(sum 1 5)",
    "(square 2)",
    "(sum (square 2) 1)",
])
def test_native_functions(expr):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number

@pytest.mark.parametrize("expr", [
    """
    (begin
        (var value 100)
        
        (def calc ((x number) (y number)) -> fn<number<number>>
            (begin
                (var z (+ x y))
                
                (def inner ((foo number)) -> number
                    (+ (+ foo z) value))
                    
                inner
            
            ))
            
        (var fn (calc 10 20))
        (fn 30))
    """,
])
def test_nested_functions(expr):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number

@pytest.mark.parametrize("expr", [
    """
    (begin
        (def factorial ((x number)) -> number
            (if (== x 1)
                1
                (* x (factorial (- x 1)))))
        
        (factorial 5))
    """,
])
def test_recursive_functions(expr):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number

@pytest.mark.parametrize("expr, type_", [
    ("""
    (lambda ((x number)) -> number (* x x))
    """, Type.from_string("fn<number<number>>")),
    ("""
    (begin
        (def onClick ((callback fn<number<number>>)) -> number
            (begin
                (var x 10)
                (var y 20)
                (callback (+ x y))))
    
        (onClick (lambda ((data number)) -> number (* data 10))))
    """, Type.number),
    ("""
    ((lambda ((x number)) -> number (* x x)) 2)
    """, Type.number),
    ("""
    (begin
        (var square (lambda ((x number)) -> number (* x x)))
        (square 2))
    """, Type.number),
])
def test_lambda_functions(expr, type_):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == type_
