import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


@pytest.mark.parametrize("expr", [1, 42, 3.5])
def test_typecheck_numbers(expr):
    evatc = EvaTC()
    assert evatc.tc(expr) == Type.number

@pytest.mark.parametrize("expr", ['"hello"', '"42"'])
def test_typecheck_strings(expr):
    evatc = EvaTC()
    assert evatc.tc(expr) == Type.string

@pytest.mark.parametrize("expr", ["true", "false"])
def test_typecheck_strings(expr):
    evatc = EvaTC()
    assert evatc.tc(expr) == Type.boolean
