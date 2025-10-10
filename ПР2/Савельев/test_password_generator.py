import unittest
from password_generator import *

class TestPasswordGenerator(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Выполняется один раз перед всеми тестами - генерируем ОДИН пароль"""
        cls.test_password = generate_password(10)
        print(f"=== Тестирование генератора паролей ===")
        print(f"Сгенерированный пароль: {cls.test_password}")
        print()
    
    def test_password_length(self):
        """Тест длины сгенерированного пароля"""
        self.assertEqual(len(self.test_password), 10)
        print(f"Тест длины: {self.test_password} - длина {len(self.test_password)}")
    
    def test_password_charset(self):
        """Тест что пароль содержит только разрешенные символы"""
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for char in self.test_password:
            self.assertIn(char, allowed_chars)
        print(f"Тест символов: {self.test_password} - все символы разрешены")
    
    def test_check_length_function(self):
        """Тест функции проверки длины"""
        # Тестируем функцию check_length с разными паролями
        self.assertTrue(check_length("abcdef", 6))
        self.assertTrue(check_length("abcdefgh", 6))
        self.assertFalse(check_length("abc", 6))
        self.assertFalse(check_length("", 1))
        print("Тест check_length: функция работает корректно")
    
    def test_has_uppercase_function(self):
        """Тест функции проверки заглавных букв"""
        # Тестируем функцию has_uppercase с разными паролями
        self.assertTrue(has_uppercase("Abc"))
        self.assertTrue(has_uppercase("abcD"))
        self.assertFalse(has_uppercase("abc"))
        self.assertFalse(has_uppercase("123"))
        print("Тест has_uppercase: функция работает корректно")
    
    def test_has_digits_function(self):
        """Тест функции проверки цифр"""
        # Тестируем функцию has_digits с разными паролями
        self.assertTrue(has_digits("abc123"))
        self.assertTrue(has_digits("1abc"))
        self.assertTrue(has_digits("abc0def"))
        self.assertFalse(has_digits("abc"))
        self.assertFalse(has_digits("ABC"))
        print("Тест has_digits: функция работает корректно")
    
    def test_validate_password_consistency(self):
        """
        Тест согласованности валидации пароля
        Проверяем, что validate_password дает логичные результаты
        """
        # Анализируем сгенерированный пароль
        length_ok = check_length(self.test_password, 6)
        has_upper = has_uppercase(self.test_password)
        has_digit = has_digits(self.test_password)
        
        print(f"Анализ пароля {self.test_password}:")
        print(f"  - Длина >= 6: {length_ok}")
        print(f"  - Есть заглавные: {has_upper}") 
        print(f"  - Есть цифры: {has_digit}")
        
        # Ожидаемая логика: пароль валиден если все три условия выполнены
        expected_valid = length_ok and has_upper and has_digit
        actual_valid = validate_password(self.test_password)
        
        print(f"  - Ожидаемый результат: {expected_valid}")
        print(f"  - Фактический результат: {actual_valid}")
        
        # Проверяем согласованность
        self.assertEqual(actual_valid, expected_valid, 
                        f"Несогласованность: для пароля {self.test_password} "
                        f"ожидалось {expected_valid}, но получено {actual_valid}")
    
    def test_validate_password_with_known_cases(self):
        """
        Тест валидации с заранее известными случаями
        """
        test_cases = [
            # (пароль, ожидаемый_результат, описание)
            ("Short1", True, "Короткий но соответствует всем правилам"),
            ("NoDigit", False, "Нет цифр"),
            ("nocaps123", False, "Нет заглавных букв"),
            ("GoodPass123", True, "Соответствует всем правилам"),
        ]
        
        for password, expected, description in test_cases:
            with self.subTest(password=password, description=description):
                result = validate_password(password)
                self.assertEqual(result, expected, 
                               f"Пароль '{password}': {description}. "
                               f"Ожидалось {expected}, получено {result}")

if __name__ == '__main__':
    unittest.main()