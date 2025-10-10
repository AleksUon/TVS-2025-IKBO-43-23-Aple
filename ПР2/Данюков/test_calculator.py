import pytest
from calculator import add, subtract, multiply, divide, power

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(2.5, 3.5) == 6.0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5
    assert subtract(10, 10) == 0
    assert subtract(3.5, 1.5) == 2.0

def test_multiply():
    assert multiply(4, 5) == 20
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0
    assert multiply(2.5, 4) == 10.0

def test_divide():
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5
    assert divide(0, 5) == 0
    assert divide(1, 4) == 0.25

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(5, 0)

def test_power_positive_exponent():
    assert power(2, 3) == 8
    assert power(5, 0) == 1
    assert power(3, 1) == 3
    assert power(10, 2) == 100

def test_power_negative_exponent():
    assert power(2, -1) == 0.5
    assert power(4, -2) == 0.0625
    assert power(10, -1) == 0.1