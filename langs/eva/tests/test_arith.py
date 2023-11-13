import pytest
from evalang import Eva


@pytest.mark.parametrize("expr, expected", [
    (["+", 1, 5], 6),
    (["*", 2, 4], 8),
    (["*", -1, 2], -2)
])
def test_eval_arith(expr, expected):
    eva = Eva()
    assert eva.eval(expr) == expected

@pytest.mark.parametrize("expr, expected", [
    (["+", ["+", 3, 2], 5], 10),
])
def test_eval_arith_nested(expr, expected):
    eva = Eva()
    assert eva.eval(expr) == expected
