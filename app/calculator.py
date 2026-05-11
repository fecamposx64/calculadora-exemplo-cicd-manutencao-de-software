"""
Lógica de negócio da calculadora.

Mantemos a regra separada da camada HTTP (main.py) para que ela possa
ser testada de forma 100% unitária (sem subir servidor).
"""


def add(a: float, b: float) -> float:
    """Soma dois números."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtrai b de a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiplica dois números."""
    return a * b


def divide(a: float, b: float) -> float:
    """
    Divide a por b.

    Levanta ValueError quando b é zero — esse caso de borda é
    coberto explicitamente nos testes (ver tests/test_calculator.py).
    """
    if b == 0:
        raise ValueError("Divisão por zero não é permitida")
    return a / b
