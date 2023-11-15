import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


def test_basic_type_declaration():
    expr = """
    (begin
        (type int number)
        (def square ((x int)) -> int (* x x))
        (square 2))
    """
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.int

