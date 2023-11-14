import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


@pytest.mark.parametrize("expr", [
    "(+ 2 3)",
    "(- 1 5)",
    "(* 4 2)",
    "(/ 2 3)",
])
def test_typecheck_numbers(expr):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number

@pytest.mark.parametrize("expr", [
    '(+ "hello" "world")',
])
def test_typecheck_string_concat(expr):
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.string
