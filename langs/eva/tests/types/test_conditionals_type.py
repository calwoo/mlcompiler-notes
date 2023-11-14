import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


@pytest.mark.parametrize("expr", [
    "(<= 3 10)",
    "(== 3 5)",
    '(!= "hello" "world")',
])
def test_basic_comparisons(expr):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.boolean

@pytest.mark.parametrize("expr", [
    """
    (begin
        (var x 10)
        (var y 20)
        (if (<= x 10)
            (set y 1)
            (set y 2))
        y)
    """,
    """
    (begin
        (var x 10)
        (while (!= x 0)
            (set x (- x 1))))
    """
])
def test_typecheck_conditionals(expr):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number
