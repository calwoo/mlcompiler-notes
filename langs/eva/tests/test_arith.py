import pytest
from evalang import eval


@pytest.mark.parametrize("expr, expected", [
    (["+", 1, 5], 6),
])
def test_eval_arith(expr, expected):
    assert eval(expr) == expected

@pytest.mark.parametrize("expr, expected", [
    (["+", ["+", 3, 2], 5], 10),
])
def test_eval_arith_nested(expr, expected):
    assert eval(expr) == expected
