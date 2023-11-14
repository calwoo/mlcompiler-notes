import pytest
from evalang.types import Type
from evalang.typecheck import EvaTC
from evalang.parse import parse


def test_function_from_string():
    t = Type.from_string("fn<number<number,string>>")
    assert t == Type.function.value(param_types=[Type.number, Type.string], return_type=Type.number)

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
