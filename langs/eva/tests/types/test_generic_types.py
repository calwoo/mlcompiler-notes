import pytest
from evalang.types import Type, TypeGenericFunctionBase
from evalang.typecheck import EvaTC
from evalang.parse import parse


def test_generic_function_type():
    expr = """
    (def combine <K> ((x K) (y K)) -> K (+ x y))
    """
    evatc = EvaTC()
    assert isinstance(evatc.tc(parse(expr)), TypeGenericFunctionBase)

def test_generic_lambda_type():
    expr = """
    (lambda <K> ((x K) (y K)) -> K (+ x y))
    """
    evatc = EvaTC()
    assert isinstance(evatc.tc(parse(expr)), TypeGenericFunctionBase)

def test_generic_explicit_polymorphism_1():
    expr = """
    (begin
        (def combine <K> ((x K) (y K)) -> K (+ x y))

        (combine <number> 2 3))
    """
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number

def test_generic_explicit_polymorphism_2():
    expr = """
    (begin
        (def combine <K> ((x K) (y K)) -> K (+ x y))

        (combine <string> "hello" "world"))
    """
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.string

def test_generic_lambdas_1():
    expr = """
    ((lambda <K> ((x K)) -> K (+ x x)) <number> 2)
    """
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.number

def test_generic_lambdas_2():
    expr = """
    ((lambda <K> ((x K)) -> K (+ x x)) <string> "hello")
    """
    evatc = EvaTC()
    assert evatc.tc(parse(expr)) == Type.string
