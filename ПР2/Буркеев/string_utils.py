import re
import unittest
import io
import sys
from types import FunctionType
from copy import deepcopy


# =========================
#   ПРОИЗВОДСТВЕННЫЕ ФУНКЦИИ
# =========================

def is_palindrome(s: str) -> bool:
    """
    Палиндром по буквам/цифрам, регистр игнорируется.
    Примеры:
      "А роза упала на лапу Азора" -> True
      "No lemon, no melon" -> True
      "abc" -> False
    """
    cleaned = re.sub(r'[^0-9A-Za-zА-Яа-яЁё]', '', s, flags=re.UNICODE)
    cleaned = cleaned.lower()
    return cleaned == cleaned[::-1]


def word_count(s: str) -> dict:
    """
    Подсчёт слов, регистр игнорируется, разделение по любым пробелам.
    Пример: "Hi hi HI" -> {"hi": 3}
    """
    words = re.findall(r'\w+', s.lower(), flags=re.UNICODE)
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq


def reverse_words(s: str) -> str:
    """
    Перестановка слов в обратном порядке (слова разделены пробелами),
    последовательность пробелов схлопывается до одиночного.
    Пример: "alpha   beta   gamma" -> "gamma beta alpha"
    """
    parts = s.split()
    parts.reverse()
    return " ".join(parts)


def snake_to_camel(s: str) -> str:
    """
    Конвертация snake_case -> camelCase.
    НАМЕРЕННАЯ ОШИБКА: реализация делает PascalCase (первая буква тоже заглавная).
    Пример ожидаемого поведения: "hello_world" -> "helloWorld"
    Фактическая ошибка: "hello_world" -> "HelloWorld"
    """
    parts = [p for p in s.split('_') if p != ""]
    # Ошибка: первая часть тоже capitalized -> PascalCase вместо camelCase
    return "".join(p.capitalize() for p in parts)


def compress_runs(s: str) -> str:
    """
    RLE-сжатие подряд идущих символов: "aaabcccc" -> "a3b1c4".
    Пустая строка -> "".
    """
    if not s:
        return ""
    out = []
    current = s[0]
    count = 1
    for ch in s[1:]:
        if ch == current:
            count += 1
        else:
            out.append(f"{current}{count}")
            current = ch
            count = 1
    out.append(f"{current}{count}")
    return "".join(out)


# =========================
#   МОДУЛЬНЫЕ ТЕСТЫ (unittest)
# =========================

class TestStringUtils(unittest.TestCase):
    # is_palindrome
    def test_is_palindrome_simple_true(self):
        self.assertTrue(is_palindrome("level"))

    def test_is_palindrome_simple_false(self):
        self.assertFalse(is_palindrome("python"))

    def test_is_palindrome_ignores_case_and_non_alnum(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))
        self.assertTrue(is_palindrome("А роза упала на лапу Азора"))

    # word_count
    def test_word_count_basic(self):
        self.assertEqual(word_count("Hi hi HI"), {"hi": 3})

    def test_word_count_with_punct(self):
        self.assertEqual(word_count("One, two; two!"), {"one": 1, "two": 2})

    def test_word_count_empty(self):
        self.assertEqual(word_count("   \n\t"), {})

    # reverse_words
    def test_reverse_words_basic(self):
        self.assertEqual(reverse_words("alpha beta gamma"), "gamma beta alpha")

    def test_reverse_words_collapses_spaces(self):
        self.assertEqual(reverse_words("  a   b   c  "), "c b a")

    def test_reverse_words_single(self):
        self.assertEqual(reverse_words("solo"), "solo")

    # snake_to_camel (НАМЕРЕННО ДОЛЖЕН ПРОВАЛИТЬСЯ из-за ошибки в реализации)
    def test_snake_to_camel_basic(self):
        self.assertEqual(snake_to_camel("hello_world"), "helloWorld")

    def test_snake_to_camel_single_token(self):
        self.assertEqual(snake_to_camel("value"), "value")

    def test_snake_to_camel_with_leading_trailing_underscores(self):
        self.assertEqual(snake_to_camel("__make___it__right__"), "makeItRight")

    # compress_runs
    def test_compress_runs_basic(self):
        self.assertEqual(compress_runs("aaabcccc"), "a3b1c4")

    def test_compress_runs_mixed(self):
        self.assertEqual(compress_runs("aabbaa"), "a2b2a2")

    def test_compress_runs_empty(self):
        self.assertEqual(compress_runs(""), "")


# =========================
#   ПРИМИТИВНЫЙ РАННЕР МУТАЦИОННЫХ ТЕСТОВ
# =========================
#
# Идея: для ряда функций создаём набор "мутантов" (типичные мутации),
# временно подменяем целевую функцию и прогоняем весь набор unit-тестов.
# Если тесты падают — мутант "убит". Если все тесты прошли — мутант "выжил".

def _run_unittests_silently() -> bool:
    """
    Запуск всех тестов из этого файла и возврат True, если ВСЕ прошли.
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestStringUtils)
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=0)
    result = runner.run(suite)
    return result.wasSuccessful()


def _with_patched_function(name: str, fn: FunctionType, callable_):
    """
    Контекстная подмена функции в globals() с последующим откатом.
    Реализовано вручную без менеджера контекста для лаконичности.
    """
    original = globals()[name]
    globals()[name] = fn
    try:
        return callable_()
    finally:
        globals()[name] = original


# --- Мутанты ---

# 1) is_palindrome: убираем нормализацию (типичная мутация — удалить обработку ввода)
def mutant_is_palindrome_no_normalization(s: str) -> bool:
    return s == s[::-1]

# 2) is_palindrome: инвертируем условие (== -> !=)
def mutant_is_palindrome_inverted(s: str) -> bool:
    cleaned = re.sub(r'[^0-9A-Za-zА-Яа-яЁё]', '', s, flags=re.UNICODE).lower()
    return cleaned != cleaned[::-1]

# 3) word_count: считаем без .lower() (типичная мутация — убрать понижение регистра)
def mutant_word_count_case_sensitive(s: str) -> dict:
    words = re.findall(r'\w+', s, flags=re.UNICODE)
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq

# 4) reverse_words: вместо разворота слов разворачиваем символы всей строки
def mutant_reverse_words_chars(s: str) -> str:
    return s[::-1].strip()

# 5) compress_runs: возвращаем исходную строку (мутация "возврат константы/входа")
def mutant_compress_runs_identity(s: str) -> str:
    return s


_MUTANTS = [
    ("is_palindrome", mutant_is_palindrome_no_normalization, "is_palindrome: remove normalization"),
    ("is_palindrome", mutant_is_palindrome_inverted, "is_palindrome: invert equality"),
    ("word_count", mutant_word_count_case_sensitive, "word_count: case-sensitive counting"),
    ("reverse_words", mutant_reverse_words_chars, "reverse_words: reverse chars instead of words"),
    ("compress_runs", mutant_compress_runs_identity, "compress_runs: identity"),
    # Обратите внимание: мы умышленно не создаём мутанта для snake_to_camel,
    # т.к. текущая реализация уже содержит ошибку.
]


def run_mutation_tests() -> list[tuple[str, bool]]:
    """
    Возвращает список (описание, killed: bool).
    """
    results = []
    for target_name, mutant_fn, description in _MUTANTS:
        def _execute():
            ok = _run_unittests_silently()
            # Если все тесты прошли на мутанте — мутант выжил (killed=False)
            # Если хоть один тест упал — мутант убит (killed=True)
            return not ok
        killed = _with_patched_function(target_name, mutant_fn, _execute)
        results.append((description, killed))
    return results


# =========================
#   ТОЧКА ВХОДА
# =========================

if __name__ == "__main__":
    # 1) Запуск модульных тестов
    print("=== UNIT-TESTS ===")
    success = _run_unittests_silently()
    print(f"All unit tests passed: {success}")

    # 2) Запуск мутационных тестов
    print("\n=== MUTATION TESTS ===")
    outcomes = run_mutation_tests()
    for desc, killed in outcomes:
        status = "KILLED" if killed else "SURVIVED"
        print(f"{desc}: {status}")
