import pytest
from evalang import Eva


def test_block_basic():
    block = ["begin",
        ["var", "x", 10],
        ["var", "y", 20],
        ['+', ['*', 'x', 'y'], 30],
    ]
    
    eva = Eva()
    assert eva.eval(block) == 230

@pytest.mark.parametrize("expr, expected", [
    (["begin",
        ["var", "x", 10],
        ["begin",
            ["var", "x", 20],
            "x" 
        ],
        "x"
    ], 10),
    (["begin",
        ["var", "value", 10],
        ["var", "result", ["begin",
            ["var", "x", ['+', "value", 10]],
            "x" 
        ]],
        "result"
    ], 20),
    (["begin",
        ["var", "data", 10],
        ["begin",
            ["set", "data", 100],
        ],
        "data"
    ], 100),
])
def test_block_nested(expr, expected):
    eva = Eva()
    assert eva.eval(expr) == expected
