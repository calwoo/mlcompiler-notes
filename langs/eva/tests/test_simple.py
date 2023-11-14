import pytest
from evalang import Eva
from evalang.parse import parse


@pytest.mark.parametrize("expr", [1, -1, 0, 3, 5]) 
def test_eval_numbers_basic(expr):
    eva = Eva()
    assert eva.eval(expr) == expr

@pytest.mark.parametrize("expr, expected", [
    ('"hello"', "hello"),
    ('"world"', 'world')
])
def test_eval_strings_basic(expr, expected):
    eva = Eva()
    assert eva.eval(expr) == expected
