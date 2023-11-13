import pytest
from evalang import eval


@pytest.mark.parametrize("expr", [1, -1, 0, 3, 5]) 
def test_eval_numbers_basic(expr):
    assert eval(expr) == expr

@pytest.mark.parametrize("expr, expected", [
    ('"hello"', "hello"),
    ('"world"', 'world')
])
def test_eval_strings_basic(expr, expected):
    assert eval(expr) == expected
