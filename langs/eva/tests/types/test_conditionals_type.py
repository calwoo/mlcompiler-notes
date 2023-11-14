import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


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
])
def test_typecheck_blocks(expr):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number
