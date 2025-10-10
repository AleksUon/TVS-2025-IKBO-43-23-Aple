import sys
import os

# Добавляем путь к модулю для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Converter import *


class UnitConverterTester:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []

    def run_test(self, test_function, test_name):
        """Запускает один тест и записывает результат"""
        self.total_tests += 1
        try:
            result = test_function()
            if result:
                self.passed_tests += 1
                self.test_results.append(f"ПРОЙДЕН: {test_name}")
                print(f"ПРОЙДЕН: {test_name}")
                return True
            else:
                self.failed_tests += 1
                self.test_results.append(f"ПРОВАЛЕН: {test_name}")
                print(f"ПРОВАЛЕН: {test_name}")
                return False
        except Exception as e:
            self.failed_tests += 1
            self.test_results.append(f"ОШИБКА: {test_name} - {str(e)}")
            print(f"ОШИБКА: {test_name} - {str(e)}")
            return False

    def assert_approx_equal(self, actual, expected, tolerance=0.01, message=""):
        """Проверяет приблизительное равенство с заданной точностью"""
        if abs(actual - expected) <= tolerance:
            return True
        else:
            print(f"  Ожидалось: {expected}, Получено: {actual}, Разница: {abs(actual - expected)}")
            return False

    def test_celsius_to_fahrenheit(self):
        """Тест конвертации Цельсий в Фаренгейт"""
        # Тест 1: 0°C = 32°F
        result1 = celsius_to_fahrenheit(0)
        if not self.assert_approx_equal(result1, 32):
            return False

        # Тест 2: 100°C = 212°F
        result2 = celsius_to_fahrenheit(100)
        if not self.assert_approx_equal(result2, 212):
            return False

        # Тест 3: -40°C = -40°F
        result3 = celsius_to_fahrenheit(-40)
        if not self.assert_approx_equal(result3, -40):
            return False

        # Тест 4: 37°C (температура тела) ≈ 98.6°F
        result4 = celsius_to_fahrenheit(37)
        if not self.assert_approx_equal(result4, 98.6, 0.1):
            return False

        return True

    def test_fahrenheit_to_celsius(self):
        """Тест конвертации Фаренгейт в Цельсий"""
        # Тест 1: 32°F = 0°C
        result1 = fahrenheit_to_celsius(32)
        if not self.assert_approx_equal(result1, 0):
            return False

        # Тест 2: 212°F = 100°C
        result2 = fahrenheit_to_celsius(212)
        if not self.assert_approx_equal(result2, 100):
            return False

        # Тест 3: -40°F = -40°C
        result3 = fahrenheit_to_celsius(-40)
        if not self.assert_approx_equal(result3, -40):
            return False

        # Тест 4: 98.6°F ≈ 37°C
        result4 = fahrenheit_to_celsius(98.6)
        if not self.assert_approx_equal(result4, 37, 0.1):
            return False

        return True

    def test_meters_to_feet(self):
        """Тест конвертации метров в футы"""
        # Тест 1: 1 м = 3.28084 футов
        result1 = meters_to_feet(1)
        if not self.assert_approx_equal(result1, 3.28084):
            return False

        # Тест 2: 10 м = 32.8084 футов
        result2 = meters_to_feet(10)
        if not self.assert_approx_equal(result2, 32.8084):
            return False

        # Тест 3: 0 м = 0 футов
        result3 = meters_to_feet(0)
        if not self.assert_approx_equal(result3, 0):
            return False

        return True

    def test_feet_to_meters(self):
        """Тест конвертации футов в метры"""
        # Тест 1: 3.28084 футов = 1 м
        result1 = feet_to_meters(3.28084)
        if not self.assert_approx_equal(result1, 1, 0.0001):
            return False

        # Тест 2: 10 футов ≈ 3.048 м
        result2 = feet_to_meters(10)
        if not self.assert_approx_equal(result2, 3.048, 0.001):
            return False

        # Тест 3: 0 футов = 0 м
        result3 = feet_to_meters(0)
        if not self.assert_approx_equal(result3, 0):
            return False

        return True

    def test_kilograms_to_pounds(self):
        """Тест конвертации килограммов в фунты"""
        # Тест 1: 1 кг = 2.20462 фунтов
        result1 = kilograms_to_pounds(1)
        if not self.assert_approx_equal(result1, 2.20462):
            return False

        # Тест 2: 10 кг = 22.0462 фунтов
        result2 = kilograms_to_pounds(10)
        if not self.assert_approx_equal(result2, 22.0462):
            return False

        # Тест 3: 0 кг = 0 фунтов
        result3 = kilograms_to_pounds(0)
        if not self.assert_approx_equal(result3, 0):
            return False

        return True

    def test_pounds_to_kilograms(self):
        """Тест конвертации фунтов в килограммы"""
        # Тест 1: 2.20462 фунтов = 1 кг
        result1 = pounds_to_kilograms(2.20462)
        if not self.assert_approx_equal(result1, 1, 0.0001):
            return False

        # Тест 2: 10 фунтов ≈ 4.53592 кг
        result2 = pounds_to_kilograms(10)
        if not self.assert_approx_equal(result2, 4.53592, 0.001):
            return False

        # Тест 3: 0 фунтов = 0 кг
        result3 = pounds_to_kilograms(0)
        if not self.assert_approx_equal(result3, 0):
            return False

        return True

    def test_kilometers_to_miles(self):
        """Тест конвертации километров в мили"""
        # Тест 1: 1 км = 0.621371 миль
        result1 = kilometers_to_miles(1)
        if not self.assert_approx_equal(result1, 0.621371):
            return False

        # Тест 2: 10 км = 6.21371 миль
        result2 = kilometers_to_miles(10)
        if not self.assert_approx_equal(result2, 6.21371):
            return False

        # Тест 3: 0 км = 0 миль
        result3 = kilometers_to_miles(0)
        if not self.assert_approx_equal(result3, 0):
            return False

        return True

    def test_miles_to_kilometers(self):
        """Тест конвертации миль в километры"""
        # Тест 1: 0.621371 миль = 1 км
        result1 = miles_to_kilometers(0.621371)
        if not self.assert_approx_equal(result1, 1, 0.0001):
            return False

        # Тест 2: 10 миль = 16.0934 км
        result2 = miles_to_kilometers(10)
        if not self.assert_approx_equal(result2, 16.0934, 0.001):
            return False

        # Тест 3: 0 миль = 0 км
        result3 = miles_to_kilometers(0)
        if not self.assert_approx_equal(result3, 0):
            return False

        return True

    def test_liters_to_gallons(self):
        """Тест конвертации литров в галлоны"""
        # Тест 1: 1 литр = 0.264172 галлонов
        result1 = liters_to_gallons(1)
        if not self.assert_approx_equal(result1, 0.264172):
            return False

        # Тест 2: 10 литров = 2.64172 галлонов
        result2 = liters_to_gallons(10)
        if not self.assert_approx_equal(result2, 2.64172):
            return False

        # Тест 3: 0 литров = 0 галлонов
        result3 = liters_to_gallons(0)
        if not self.assert_approx_equal(result3, 0):
            return False

        return True

    def test_gallons_to_liters(self):
        """Тест конвертации галлонов в литры"""
        # Тест 1: 0.264172 галлонов = 1 литр
        result1 = gallons_to_liters(0.264172)
        if not self.assert_approx_equal(result1, 1, 0.0001):
            return False

        # Тест 2: 10 галлонов = 37.8541 литров
        result2 = gallons_to_liters(10)
        if not self.assert_approx_equal(result2, 37.8541, 0.001):
            return False

        # Тест 3: 0 галлонов = 0 литров
        result3 = gallons_to_liters(0)
        if not self.assert_approx_equal(result3, 0):
            return False

        return True

    def test_perform_conversion(self):
        """Тест функции perform_conversion"""
        # Тест различных типов конвертаций
        test_cases = [
            (1, 0, 32),  # Celsius to Fahrenheit
            (2, 32, 0),  # Fahrenheit to Celsius
            (3, 1, 3.28084),  # Meters to Feet
            (5, 1, 2.20462),  # Kilograms to Pounds
            (7, 1, 0.621371),  # Kilometers to Miles
            (9, 1, 0.264172),  # Liters to Gallons
        ]

        for choice, input_val, expected in test_cases:
            result, description = perform_conversion(choice, input_val)
            if not self.assert_approx_equal(result, expected, 0.001):
                print(f"  Ошибка в конвертации типа {choice}")
                return False

        # Тест неверного выбора
        result, description = perform_conversion(99, 10)
        if result is not None:
            print("  Ожидался None для неверного выбора")
            return False

        return True

    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Тест отрицательных значений
        try:
            result1 = celsius_to_fahrenheit(-100)
            result2 = meters_to_feet(-5)
            result3 = kilograms_to_pounds(-10)

            # Проверяем, что функции не падают на отрицательных значениях
            # (не проверяем корректность результата, только отсутствие исключений)
            return True
        except Exception as e:
            print(f"  Ошибка при обработке отрицательных значений: {e}")
            return False

    def run_all_tests(self):
        """Запускает все тесты и выводит отчет"""
        print("Запуск модульного тестирования конвертера единиц измерения")
        print("=" * 60)

        # Запуск всех тестов
        tests = [
            (self.test_celsius_to_fahrenheit, "Конвертация Цельсий -> Фаренгейт"),
            (self.test_fahrenheit_to_celsius, "Конвертация Фаренгейт -> Цельсий"),
            (self.test_meters_to_feet, "Конвертация метров -> футы"),
            (self.test_feet_to_meters, "Конвертация футов -> метры"),
            (self.test_kilograms_to_pounds, "Конвертация килограммов -> фунты"),
            (self.test_pounds_to_kilograms, "Конвертация фунтов -> килограммы"),
            (self.test_kilometers_to_miles, "Конвертация километров -> мили"),
            (self.test_miles_to_kilometers, "Конвертация миль -> километры"),
            (self.test_liters_to_gallons, "Конвертация литров -> галлоны"),
            (self.test_gallons_to_liters, "Конвертация галлонов -> литры"),
            (self.test_edge_cases, "Граничные случаи"),
        ]

        for test_func, test_name in tests:
            self.run_test(test_func, test_name)

        # Вывод итогового отчета
        print("\n" + "=" * 60)
        print("ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
        print("=" * 60)
        print(f"Всего тестов: {self.total_tests}")
        print(f"Пройдено: {self.passed_tests}")
        print(f"Провалено: {self.failed_tests}")

        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        print(f"Успешность: {success_rate:.1f}%")

        if self.failed_tests > 0:
            print("\nДетали проваленных тестов:")
            for result in self.test_results:
                if result.startswith("ПРОВАЛЕН") or result.startswith("ОШИБКА"):
                    print(f"  - {result}")

        return self.failed_tests == 0


def main():
    """Основная функция для запуска тестов"""
    tester = UnitConverterTester()
    success = tester.run_all_tests()

    if success:
        print("\nСтатус: Все тесты пройдены успешно!")
        sys.exit(0)
    else:
        print("\nСтатус: Обнаружены ошибки в модуле!")
        sys.exit(1)


if __name__ == "__main__":
    main()