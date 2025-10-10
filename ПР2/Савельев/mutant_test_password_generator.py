"""
Мутационное тестирование - оценка качества тестов
"""

import unittest
import importlib.util
import sys
import os

class MutationTester:
    def __init__(self):
        self.results = []
        
    def create_mutant(self, source_file, changes):
        """Создает измененную версию кода"""
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for old_text, new_text in changes.items():
            content = content.replace(old_text, new_text)
        
        mutant_file = 'mutant_temp.py'
        with open(mutant_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return mutant_file
    
    def run_tests_on_mutant(self, mutant_file, test_file):
        """Запускает тесты на измененной версии кода"""
        try:
            # Загружаем измененный модуль
            spec = importlib.util.spec_from_file_location("password_generator", mutant_file)
            mutant_module = importlib.util.module_from_spec(spec)
            sys.modules["password_generator"] = mutant_module
            spec.loader.exec_module(mutant_module)
            
            # Загружаем тесты
            test_spec = importlib.util.spec_from_file_location("test_module", test_file)
            test_module = importlib.util.module_from_spec(test_spec)
            test_spec.loader.exec_module(test_module)
            
            # Запускаем тесты
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(test_module)
            runner = unittest.TextTestRunner(verbosity=0)
            result = runner.run(suite)
            
            return result
            
        except Exception as e:
            return None
        finally:
            if os.path.exists(mutant_file):
                os.remove(mutant_file)
    
    def run_quality_assessment(self):
        """Запускает оценку качества тестов"""
        print("Оценка качества тестового покрытия")
        print("=" * 50)
        
        # Изменения для проверки чувствительности тестов
        modifications = [
            {
                "description": "Изменение проверки минимальной длины",
                "changes": {"len(password) >= min_length": "len(password) > min_length"}
            },
            {
                "description": "Изменение логики проверки заглавных букв",
                "changes": {"if char.isupper():": "if not char.isupper():"}
            },
            {
                "description": "Изменение логики проверки цифр", 
                "changes": {"if char.isdigit():": "if not char.isdigit():"}
            },
            {
                "description": "Ослабление требований к длине пароля",
                "changes": {"len(password) < 6": "len(password) < 4"}
            },
            {
                "description": "Изменение состава допустимых символов",
                "changes": {"string.ascii_letters + string.digits": "string.ascii_lowercase + string.digits"}
            }
        ]
        
        modifications_detected = 0
        modifications_missed = 0
        
        print("Проверка чувствительности тестов к изменениям кода...")
        print("-" * 50)
        
        for i, modification in enumerate(modifications, 1):
            print(f"Изменение {i}: {modification['description']}")
            
            # Создаем измененную версию
            mutant_file = self.create_mutant("password_generator.py", modification["changes"])
            
            # Запускаем тесты
            result = self.run_tests_on_mutant(mutant_file, "test_password_generator.py")
            
            # Анализируем результаты
            if result and (result.failures or result.errors):
                modifications_detected += 1
                status = "ОБНАРУЖЕНО"
                print(f"Результат: {status} - тесты отреагировали на изменение")
            else:
                modifications_missed += 1
                status = "ПРОПУЩЕНО"
                print(f"Результат: {status} - тесты не отреагировали на изменение")
            
            self.results.append({
                "number": i,
                "description": modification["description"],
                "status": status
            })
            print()
        
        # Анализ качества
        print("=" * 50)
        print("РЕЗУЛЬТАТЫ ОЦЕНКИ КАЧЕСТВА ТЕСТОВ")
        print("=" * 50)
        
        total_modifications = len(modifications)
        detection_rate = (modifications_detected / total_modifications) * 100
        
        print(f"Всего внесено изменений: {total_modifications}")
        print(f"Изменений обнаружено: {modifications_detected}")
        print(f"Изменений пропущено: {modifications_missed}")
        print(f"Эффективность обнаружения: {detection_rate:.1f}%")
        
        print("\nДетальный отчет по изменениям:")
        for result in self.results:
            print(f"{result['number']}. {result['description']}: {result['status']}")
        
        # Вывод рекомендаций
        print("\nАНАЛИЗ ТЕСТОВОГО ПОКРЫТИЯ:")
        if detection_rate >= 80:
            print("Высокое качество тестов - тесты хорошо обнаруживают изменения в коде")
        elif detection_rate >= 60:
            print("Хорошее качество тестов - большинство изменений обнаруживается")
        elif detection_rate >= 40:
            print("Удовлетворительное качество тестов - требуется улучшение покрытия")
        else:
            print("Низкое качество тестов - необходимо добавить тесты для ключевых функциональностей")

def main():
    """Основная функция"""
    # Проверяем наличие необходимых файлов
    if not os.path.exists('password_generator.py'):
        print("Ошибка: основной модуль не найден")
        return
        
    if not os.path.exists('test_password_generator.py'):
        print("Ошибка: тестовый модуль не найден")
        return
    
    print("Запуск оценки качества тестового покрытия...")
    print("Этот процесс проверяет, насколько хорошо тесты обнаруживают изменения в коде.")
    print()
    
    # Запускаем оценку
    tester = MutationTester()
    tester.run_quality_assessment()

if __name__ == "__main__":
    main()