import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


def test_union_type_1():
    expr = """
    (begin
        (type value (or number string))
        (type ID (or string number))
        
        (var (x value) 10)
        x)
    """
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.value
    assert evatc.tc(parse(expr)) == Type.number
    assert evatc.tc(parse(expr)) == Type.string

def test_union_type_2():
    expr = """
    (begin
        (type value (or number string))
        (type ID (or string number))

        (var (a value) 10)
        (var (b ID) "x")
        
        (def process ((id ID)) -> number
            (+ a id))
        
        (process b)
        (+ a b))
    """
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number

def test_union_type_3():
    expr = """
    (begin
        (type value (or number string))
        (type ID (or string number))

        (var (a value) 10)
        (var (b ID) "x")
        
        (def process ((id ID)) -> number
            (- a id))
        
        (process b)
        (+ a b))
    """
    with pytest.raises(Exception):
        evatc = EvaTC()
        evatc.tc(parse(expr))
