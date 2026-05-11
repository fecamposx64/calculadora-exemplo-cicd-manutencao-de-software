"""
Testes unitários para app/calculator.py

Estes são "testes puros": não dependem de HTTP, banco, ou qualquer recurso
externo. Rodam em milissegundos — exatamente o tipo de teste que faz o
pipeline ser rápido e confiável.
"""

import pytest

from app import calculator


class TestAdd:
    def test_dois_positivos(self):
        assert calculator.add(2, 3) == 5

    def test_com_negativo(self):
        assert calculator.add(-5, 3) == -2

    def test_zero(self):
        assert calculator.add(0, 0) == 0


class TestSubtract:
    def test_resultado_positivo(self):
        assert calculator.subtract(10, 4) == 6

    def test_resultado_negativo(self):
        assert calculator.subtract(3, 10) == -7


class TestMultiply:
    def test_dois_positivos(self):
        assert calculator.multiply(4, 5) == 20

    def test_por_zero(self):
        assert calculator.multiply(99, 0) == 0

    def test_negativo_por_positivo(self):
        assert calculator.multiply(-3, 4) == -12


class TestDivide:
    def test_divisao_exata(self):
        assert calculator.divide(10, 2) == 5

    def test_divisao_com_resto(self):
        assert calculator.divide(7, 2) == 3.5

    def test_divisao_por_zero_levanta_erro(self):
        # Caso de borda crítico: o teste garante que o erro é capturado
        # corretamente, evitando que a divisão por zero quebre a API.
        with pytest.raises(ValueError, match="Divisão por zero"):
            calculator.divide(10, 0)
