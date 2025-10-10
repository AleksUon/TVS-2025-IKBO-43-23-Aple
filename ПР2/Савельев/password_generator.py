import random
import string

def generate_password(length=8):
    """Генерирует случайный пароль"""
    chars = string.ascii_letters + string.digits
    password = ''
    for i in range(length):
        password += random.choice(chars)
    return password

def check_length(password, min_length=6):
    """Проверяет длину пароля"""
    return len(password) >= min_length

def has_uppercase(password):
    """Проверяет наличие заглавных букв"""
    for char in password:
        if char.isupper():
            return True
    return False

def has_digits(password):
    """Проверяет наличие цифр"""
    for char in password:
        if char.isdigit():
            return True
    return False

def validate_password(password):
    """
    Функция с преднамеренной ошибкой
    Проверяет пароль на соответствие правилам
    """
    # Правило 1: длина не менее 6 символов
    if len(password) < 6:
        return False
    
    # Правило 2: должна быть хотя бы одна заглавная буква
    if not has_uppercase(password):
        return False
    
    # Правило 3: должна быть хотя бы 1 цифра
    has_digit = False
    for char in password:
        if char == '1':
            has_digit = True
            break
    
    if not has_digit:
        return False
    
    return True