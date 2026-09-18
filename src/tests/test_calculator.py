"""
Calculator app tests
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from unittest.mock import mock_open, patch
import pytest
from calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# --- Initialisation & Message d'accueil ---

def test_app():
    my_calculator = Calculator()
    welcome_message = my_calculator.get_hello_message()
    assert "== Calculatrice v1.0 ==" in welcome_message


def test_init(calc):
    assert calc.last_result == 0


def test_hello_message_with_env(calc):
    mock_env = "CALCULATOR_USERNAME=Alice\n"
    with patch("builtins.open", mock_open(read_data=mock_env)):
        message = calc.get_hello_message()
    assert "== Calculatrice v1.0 ==" in message
    assert "Bienvenu(e) Alice" in message


def test_hello_message_without_env(calc):
    with patch("builtins.open", side_effect=FileNotFoundError):
        message = calc.get_hello_message()
    assert "== Calculatrice v1.0 ==" in message
    assert "Bienvenu(e)" not in message


# --- Addition ---

def test_addition():
    my_calculator = Calculator()
    assert my_calculator.addition(2, 3) == 5


def test_addition_negative_numbers(calc):
    assert calc.addition(-2, -3) == -5
    assert calc.addition(-5, 10) == 5
    assert calc.last_result == 5


def test_addition_floats(calc):
    assert calc.addition(1.5, 2.5) == pytest.approx(4.0)


# --- Soustraction ---

def test_subtraction(calc):
    assert calc.subtraction(5, 3) == 2
    assert calc.last_result == 2


def test_subtraction_negative_result(calc):
    assert calc.subtraction(2, 5) == -3
    assert calc.last_result == -3


def test_subtraction_negative_numbers(calc):
    assert calc.subtraction(-5, -3) == -2
    assert calc.subtraction(-5, 5) == -10


def test_subtraction_floats(calc):
    assert calc.subtraction(5.5, 2.2) == pytest.approx(3.3)


# --- Multiplication ---

def test_multiplication(calc):
    assert calc.multiplication(3, 4) == 12
    assert calc.last_result == 12


def test_multiplication_by_zero(calc):
    assert calc.multiplication(5, 0) == 0
    assert calc.last_result == 0


def test_multiplication_negative_numbers(calc):
    assert calc.multiplication(-3, 4) == -12
    assert calc.multiplication(-3, -4) == 12


def test_multiplication_floats(calc):
    assert calc.multiplication(2.5, 4.0) == pytest.approx(10.0)


# --- Division ---

def test_division(calc):
    assert calc.division(6, 3) == 2.0
    assert calc.last_result == 2.0


def test_division_float_result(calc):
    assert calc.division(5, 2) == 2.5
    assert calc.last_result == 2.5


def test_division_negative_numbers(calc):
    assert calc.division(-6, 3) == -2.0
    assert calc.division(6, -3) == -2.0
    assert calc.division(-6, -3) == 2.0


def test_division_by_zero(calc):
    result = calc.division(5, 0)
    assert result == "Erreur : division par zéro"
    assert calc.last_result == "Error"


# --- Enchaînement et état de last_result ---

def test_last_result_sequence(calc):
    calc.addition(10, 5)
    assert calc.last_result == 15
    calc.subtraction(15, 3)
    assert calc.last_result == 12
    calc.multiplication(12, 2)
    assert calc.last_result == 24
    calc.division(24, 4)
    assert calc.last_result == 6.0