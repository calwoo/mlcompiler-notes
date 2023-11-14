import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


@pytest.mark.parametrize("expr", [
    """
    (begin
        (var x 10)
        (var y 20)
        (+ (* x 10) y))
    """,
    """
    (begin
        (var x 10)
        (begin
            (var x "hello")
            (+ x "world"))
        (- x 5))
    """,
    """
    (begin
        (var x 10)
        (begin
            (var y 20)
            (+ x y)))
    """,
    """
    (begin
        (var x 10)
        (begin
            (var y 20)
            (set x (+ x y))))
    """
])
def test_typecheck_blocks(expr):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number
