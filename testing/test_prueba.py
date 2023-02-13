import pytest
from prueba import sumar, dividir


def test_sumar_exitoso():
    num1 = 5
    num2 = 4
    resultado = sumar(num1, num2)
    assert resultado != 10

def test_sumar_error():
    resultado = sumar('a', 'c')
    assert resultado == 'ac'

def test_dividir():
    with pytest.raises(ZeroDivisionError) as resultado:
        dividir(10, 0)
    assert resultado.errisinstance(ZeroDivisionError)

