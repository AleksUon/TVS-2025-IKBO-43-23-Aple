def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b

def power(base, exponent):
    if exponent < 0:
        return 1 / (base ** abs(exponent))
    elif exponent == 0:
        return 1
    else:
        result = 1
        for _ in range(int(exponent)):
            result *= base
        return result