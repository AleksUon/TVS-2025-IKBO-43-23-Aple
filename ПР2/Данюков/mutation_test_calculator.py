import sys
import os
import ast
import inspect
from typing import List, Dict, Any

# Добавляем путь к модулю для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calculator import add, subtract, multiply, divide, power


class MutationTester:
    def __init__(self):
        self.total_mutants = 0
        self.killed_mutants = 0
        self.survived_mutants = 0
        self.mutation_results = []
        self.original_functions = {}

    def save_original_functions(self):
        """Сохраняет оригинальные версии функций"""
        functions_to_test = [
            'add', 'subtract', 'multiply', 'divide', 'power'
        ]

        for func_name in functions_to_test:
            self.original_functions[func_name] = globals()[func_name]

    def restore_original_functions(self):
        """Восстанавливает оригинальные функции"""
        for func_name, func in self.original_functions.items():
            globals()[func_name] = func

    def create_test_cases(self) -> List[Dict[str, Any]]:
        """Создает тестовые случаи для проверки мутантов"""
        return [
            # add
            {'function': 'add', 'args': (2, 3), 'expected': 5},
            {'function': 'add', 'args': (-1, 1), 'expected': 0},
            {'function': 'add', 'args': (0, 0), 'expected': 0},
            {'function': 'add', 'args': (2.5, 3.5), 'expected': 6.0},
            {'function': 'add', 'args': (-5, -3), 'expected': -8},

            # subtract
            {'function': 'subtract', 'args': (5, 3), 'expected': 2},
            {'function': 'subtract', 'args': (0, 5), 'expected': -5},
            {'function': 'subtract', 'args': (10, 10), 'expected': 0},
            {'function': 'subtract', 'args': (3.5, 1.5), 'expected': 2.0},

            # multiply
            {'function': 'multiply', 'args': (4, 5), 'expected': 20},
            {'function': 'multiply', 'args': (-2, 3), 'expected': -6},
            {'function': 'multiply', 'args': (0, 5), 'expected': 0},
            {'function': 'multiply', 'args': (2.5, 4), 'expected': 10.0},

            # divide
            {'function': 'divide', 'args': (10, 2), 'expected': 5},
            {'function': 'divide', 'args': (7, 2), 'expected': 3.5},
            {'function': 'divide', 'args': (0, 5), 'expected': 0},
            {'function': 'divide', 'args': (1, 4), 'expected': 0.25},
            {'function': 'divide', 'args': (-10, 2), 'expected': -5},

            # power
            {'function': 'power', 'args': (2, 3), 'expected': 8},
            {'function': 'power', 'args': (5, 0), 'expected': 1},
            {'function': 'power', 'args': (3, 1), 'expected': 3},
            {'function': 'power', 'args': (2, -1), 'expected': 0.5},
            {'function': 'power', 'args': (4, -2), 'expected': 0.0625},
        ]

    def run_test_suite(self, test_cases: List[Dict[str, Any]]) -> bool:
        """Запускает тестовый набор для текущей версии функций"""
        try:
            for test_case in test_cases:
                func_name = test_case['function']
                args = test_case['args']
                expected = test_case['expected']

                func = globals()[func_name]
                result = func(*args)

                # Проверка с допуском 0.001 для чисел с плавающей точкой
                if isinstance(result, float) or isinstance(expected, float):
                    if abs(result - expected) > 0.001:
                        return False
                else:
                    if result != expected:
                        return False
            return True
        except Exception:
            return False

    def mutate_arithmetic_operator(self, func):
        """Мутация арифметических операторов"""
        original_source = inspect.getsource(func)

        mutations = [
            ('+', '-'), ('-', '+'), ('*', '/'), ('/', '*'),
            ('+', '*'), ('-', '/'), ('*', '+'), ('/', '-'),
            ('**', '*'), ('*', '**')
        ]

        mutated_funcs = []
        for old_op, new_op in mutations:
            if old_op in original_source:
                mutated_source = original_source.replace(old_op, new_op)
                try:
                    # Создаем мутированную функцию
                    exec(mutated_source, globals())
                    mutated_func_name = func.__name__
                    mutated_funcs.append(globals()[mutated_func_name])
                except:
                    continue

        return mutated_funcs

    def mutate_numeric_values(self, func):
        """Мутация числовых значений"""
        original_source = inspect.getsource(func)

        # Ищем числовые значения в коде
        tree = ast.parse(original_source)
        numbers = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                numbers.append(node.value)
            elif isinstance(node, ast.Num):  # Для старых версий Python
                numbers.append(node.n)

        mutated_funcs = []
        for number in set(numbers):
            if number != 0:  # Не мутируем нули
                # Мутации: инкремент, декремент, инверсия знака
                mutations = [
                    number + 1, number - 1, number * 2, number / 2,
                    -number, number + 0.1, number - 0.1, 0, 1
                ]

                for mutated_num in mutations:
                    old_str = f"{number}"
                    # Обработка чисел с плавающей точкой
                    if isinstance(number, float):
                        old_str = f"{number:.1f}" if number == int(number) else f"{number}"

                    new_str = f"{mutated_num}"
                    if isinstance(mutated_num, float):
                        new_str = f"{mutated_num:.1f}" if mutated_num == int(mutated_num) else f"{mutated_num}"

                    if old_str in original_source:
                        mutated_source = original_source.replace(old_str, new_str)
                        try:
                            exec(mutated_source, globals())
                            mutated_func_name = func.__name__
                            mutated_funcs.append(globals()[mutated_func_name])
                        except:
                            continue

        return mutated_funcs

    def mutate_comparison_operators(self, func):
        """Мутация операторов сравнения"""
        original_source = inspect.getsource(func)

        mutations = [
            ('<', '>'), ('>', '<'), ('<=', '>='), ('>=', '<='),
            ('==', '!='), ('!=', '==')
        ]

        mutated_funcs = []
        for old_op, new_op in mutations:
            if old_op in original_source:
                mutated_source = original_source.replace(old_op, new_op)
                try:
                    exec(mutated_source, globals())
                    mutated_func_name = func.__name__
                    mutated_funcs.append(globals()[mutated_func_name])
                except:
                    continue

        return mutated_funcs

    def mutate_function(self, func_name: str):
        """Создает мутации для указанной функции"""
        func = globals()[func_name]
        mutations = []

        # Сохраняем оригинальную функцию
        original_func = globals()[func_name]

        # Применяем различные типы мутаций
        mutations.extend(self.mutate_arithmetic_operator(func))
        mutations.extend(self.mutate_numeric_values(func))
        mutations.extend(self.mutate_comparison_operators(func))

        # Восстанавливаем оригинальную функцию
        globals()[func_name] = original_func

        return mutations

    def test_mutant(self, mutant_func, func_name: str, test_cases: List[Dict[str, Any]]) -> bool:
        """Тестирует одного мутанта"""
        # Сохраняем текущую функцию
        current_func = globals()[func_name]

        try:
            # Заменяем функцию мутантом
            globals()[func_name] = mutant_func

            # Запускаем тесты
            test_passed = self.run_test_suite(test_cases)

            return test_passed
        finally:
            # Восстанавливаем оригинальную функцию
            globals()[func_name] = current_func

    def run_mutation_testing(self):
        """Запускает мутационное тестирование"""
        print("Запуск мутационного тестирования калькулятора")
        print("=" * 70)

        self.save_original_functions()
        test_cases = self.create_test_cases()

        functions_to_mutate = list(self.original_functions.keys())

        for func_name in functions_to_mutate:
            print(f"\nМутационное тестирование функции: {func_name}")
            print("-" * 50)

            mutants = self.mutate_function(func_name)
            print(f"Создано мутантов: {len(mutants)}")

            for i, mutant in enumerate(mutants):
                self.total_mutants += 1

                try:
                    survived = self.test_mutant(mutant, func_name, test_cases)

                    if survived:
                        self.survived_mutants += 1
                        status = "ВЫЖИЛ"
                    else:
                        self.killed_mutants += 1
                        status = "УБИТ"

                    result_msg = f"  Мутант {i + 1}: {status}"
                    self.mutation_results.append(f"{func_name} - {result_msg}")
                    print(result_msg)

                except Exception as e:
                    self.total_mutants -= 1  # Не считаем мутантов, вызвавших ошибку
                    print(f"  Мутант {i + 1}: ОШИБКА - {str(e)}")

        # Восстанавливаем оригинальные функции
        self.restore_original_functions()

        self.generate_report()

    def generate_report(self):
        """Генерирует отчет о мутационном тестировании"""
        print("\n" + "=" * 70)
        print("ОТЧЕТ МУТАЦИОННОГО ТЕСТИРОВАНИЯ КАЛЬКУЛЯТОРА")
        print("=" * 70)

        print(f"Всего создано мутантов: {self.total_mutants}")
        print(f"Убито мутантов: {self.killed_mutants}")
        print(f"Выжило мутантов: {self.survived_mutants}")

        if self.total_mutants > 0:
            mutation_score = (self.killed_mutants / self.total_mutants) * 100
            print(f"Мутационный счет: {mutation_score:.1f}%")

        print("\nДетали результатов:")
        for result in self.mutation_results[:20]:  # Показываем первые 20 результатов
            print(f"  {result}")

        if len(self.mutation_results) > 20:
            print(f"  ... и еще {len(self.mutation_results) - 20} результатов")

        # Анализ качества тестов
        if self.total_mutants > 0:
            if mutation_score >= 80:
                print("\nСтатус: Отличное покрытие мутациями!")
            elif mutation_score >= 60:
                print("\nСтатус: Хорошее покрытие мутациями")
            elif mutation_score >= 40:
                print("\nСтатус: Удовлетворительное покрытие мутациями")
            else:
                print("\nСтатус: Низкое покрытие мутациями - нужны улучшения тестов")


class AdvancedMutationTester(MutationTester):
    """Расширенный мутационный тестер с дополнительными мутациями"""

    def mutate_logical_operators(self, func):
        """Мутация логических операторов"""
        original_source = inspect.getsource(func)

        mutations = [
            ('and', 'or'), ('or', 'and'),
        ]

        mutated_funcs = []
        for old_op, new_op in mutations:
            if old_op in original_source and old_op.strip():
                mutated_source = original_source.replace(old_op, new_op)
                try:
                    exec(mutated_source, globals())
                    mutated_func_name = func.__name__
                    mutated_funcs.append(globals()[mutated_func_name])
                except:
                    continue

        return mutated_funcs

    def mutate_assignment_operators(self, func):
        """Мутация операторов присваивания"""
        original_source = inspect.getsource(func)

        mutations = [
            ('=', '=='), ('==', '='),
        ]

        mutated_funcs = []
        for old_op, new_op in mutations:
            if old_op in original_source:
                mutated_source = original_source.replace(old_op, new_op)
                try:
                    exec(mutated_source, globals())
                    mutated_func_name = func.__name__
                    mutated_funcs.append(globals()[mutated_func_name])
                except:
                    continue

        return mutated_funcs

    def mutate_function_calls(self, func):
        """Мутация вызовов функций"""
        original_source = inspect.getsource(func)

        # Простая мутация - замена имен функций на похожие
        function_replacements = [
            ('abs', 'round'), ('round', 'abs'),
            ('int', 'float'), ('float', 'int')
        ]

        mutated_funcs = []
        for old_func, new_func in function_replacements:
            if old_func in original_source:
                mutated_source = original_source.replace(old_func, new_func)
                try:
                    exec(mutated_source, globals())
                    mutated_func_name = func.__name__
                    mutated_funcs.append(globals()[mutated_func_name])
                except:
                    continue

        return mutated_funcs

    def mutate_return_values(self, func):
        """Мутация возвращаемых значений"""
        original_source = inspect.getsource(func)

        # Мутации возвращаемых значений
        return_mutations = [
            ('return', 'return 0'),
            ('return', 'return 1'),
            ('return', 'return -1'),
            ('return', 'return None'),
        ]

        mutated_funcs = []
        for old_return, new_return in return_mutations:
            if old_return in original_source and new_return not in original_source:
                mutated_source = original_source.replace(old_return, new_return)
                try:
                    exec(mutated_source, globals())
                    mutated_func_name = func.__name__
                    mutated_funcs.append(globals()[mutated_func_name])
                except:
                    continue

        return mutated_funcs

    def mutate_function(self, func_name: str):
        """Расширенная версия создания мутаций"""
        func = globals()[func_name]
        mutations = []

        original_func = globals()[func_name]

        # Базовые мутации
        mutations.extend(self.mutate_arithmetic_operator(func))
        mutations.extend(self.mutate_numeric_values(func))
        mutations.extend(self.mutate_comparison_operators(func))

        # Расширенные мутации
        mutations.extend(self.mutate_logical_operators(func))
        mutations.extend(self.mutate_assignment_operators(func))
        mutations.extend(self.mutate_function_calls(func))
        mutations.extend(self.mutate_return_values(func))

        globals()[func_name] = original_func

        return mutations


def main():
    """Основная функция для запуска мутационного тестирования"""
    print("МУТАЦИОННОЕ ТЕСТИРОВАНИЕ КАЛЬКУЛЯТОРА")
    print("=" * 70)

    # Проверяем, что оригинальные тесты проходят
    print("Проверка оригинальных тестов...")
    tester = MutationTester()
    test_cases = tester.create_test_cases()

    if tester.run_test_suite(test_cases):
        print("✓ Оригинальные тесты проходят")
    else:
        print("✗ Оригинальные тесты не проходят! Прерывание.")
        return

    print("\nЗапуск базового мутационного тестирования...")
    basic_tester = MutationTester()
    basic_tester.run_mutation_testing()

    print("\n" + "=" * 70)
    print("ЗАПУСК РАСШИРЕННОГО МУТАЦИОННОГО ТЕСТИРОВАНИЯ")
    print("=" * 70)

    advanced_tester = AdvancedMutationTester()
    advanced_tester.run_mutation_testing()


if __name__ == "__main__":
    main()
