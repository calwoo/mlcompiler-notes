import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


def test_typecheck_vars():
    evatc = EvaTC()
    print(evatc.globalenv)
    assert evatc.tc(parse("(var x 10)")) == Type.number
    assert evatc.tc(parse("(var (x number) 10)")) == Type.number
    assert evatc.tc(parse("x")) == Type.number
    assert evatc.tc(parse("VERSION")) == Type.string

def test_raise_wrong_type_set():
    evatc = EvaTC()
    with pytest.raises(Exception):
        block = """
            (begin
                (var x 10)
                (set x "hello"))
        """
        evatc.tc(parse(block))
