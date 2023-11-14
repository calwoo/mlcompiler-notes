import pytest
from evalang import Eva


@pytest.mark.parametrize("expr, expected", [
    (["begin",
        ["var", "x", 10],
        ["var", "y", 0],
        ["if", ['>', "x", 10],
            ["set", "y", 20],
            ["set", "y", 30]],
        "y"
    ], 30),
])
def test_if(expr, expected):
    eva = Eva()
    assert eva.eval(expr) == expected

@pytest.mark.parametrize("expr, expected", [
    (["begin",
        ["var", "counter", 0],
        ["var", "result", 0],
        ["while", ['<', "counter", 10],
            ["begin",
                ["set", "result", ['+', "result", 1]],
                ["set", "counter", ['+', "counter", 1]],
            ],
        ],
        "result"
    ], 10),
])
def test_while(expr, expected):
    eva = Eva()
    assert eva.eval(expr) == expected
