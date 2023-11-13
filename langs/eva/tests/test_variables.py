import pytest
from evalang import Eva


@pytest.mark.parametrize("expr, expected", [
    (["var", "x", 10], 10),
    (["var", "isUser", "true"], True),
    (["var", "z", ['*', 2, 2]], 4)
])
def test_eval_simple_assignment(expr, expected):
    eva = Eva()
    assert eva.eval(expr) == expected

def test_var_retrieval():
    eva = Eva()
    eva.eval(["var", "x", 10])
    assert eva.eval("x") == 10

    eva.eval(["var", "y", 100])
    assert eva.eval("y") == 100

@pytest.mark.parametrize("expr, expected", [
    ("true", True), ("false", False), ("null", None)
])
def test_builtin_vars(expr, expected):
    eva = Eva()
    assert eva.eval(expr) == expected
