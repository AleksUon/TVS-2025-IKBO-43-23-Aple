def celsius_to_fahrenheit(celsius):
    """
    Конвертирует температуру из Цельсия в Фаренгейт

    Args:
        celsius (float): Температура в градусах Цельсия

    Returns:
        float: Температура в градусах Фаренгейта
    """
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):
    """
    Конвертирует температуру из Фаренгейта в Цельсий

    Args:
        fahrenheit (float): Температура в градусах Фаренгейта

    Returns:
        float: Температура в градусах Цельсия
    """
    return (fahrenheit - 32) * 5 / 9


def meters_to_feet(meters):
    """
    Конвертирует длину из метров в футы

    Args:
        meters (float): Длина в метрах

    Returns:
        float: Длина в футах
    """
    return meters * 3.28084


def feet_to_meters(feet):
    """
    Конвертирует длину из футов в метры

    Args:
        feet (float): Длина в футах

    Returns:
        float: Длина в метрах
    """
    return feet / 3.28084


def kilograms_to_pounds(kilograms):
    """
    Конвертирует массу из килограммов в фунты

    Args:
        kilograms (float): Масса в килограммах

    Returns:
        float: Масса в фунтах
    """
    # ПРЕДНАМЕРЕННАЯ ОШИБКА: неправильный коэффициент конвертации
    return kilograms * 2.20462  # Должно быть 2.20462


def pounds_to_kilograms(pounds):
    """
    Конвертирует массу из фунтов в килограммы

    Args:
        pounds (float): Масса в фунтах

    Returns:
        float: Масса в килограммах
    """
    return pounds / 2.20462


def kilometers_to_miles(kilometers):
    """
    Конвертирует расстояние из километров в мили

    Args:
        kilometers (float): Расстояние в километрах

    Returns:
        float: Расстояние в милях
    """
    return kilometers * 0.621371


def miles_to_kilometers(miles):
    """
    Конвертирует расстояние из миль в километры

    Args:
        miles (float): Расстояние в милях

    Returns:
        float: Расстояние в километрах
    """
    return miles / 0.621371


def liters_to_gallons(liters):
    """
    Конвертирует объем из литров в галлоны

    Args:
        liters (float): Объем в литрах

    Returns:
        float: Объем в галлонах
    """
    return liters * 0.264172


def gallons_to_liters(gallons):
    """
    Конвертирует объем из галлонов в литры

    Args:
        gallons (float): Объем в галлонах

    Returns:
        float: Объем в литрах
    """
    return gallons / 0.264172


def display_conversion_menu():
    """Отображает меню доступных конвертаций"""
    print("\n=== Конвертер единиц измерения ===")
    print("1. Температура: Цельсий -> Фаренгейт")
    print("2. Температура: Фаренгейт -> Цельсий")
    print("3. Длина: Метры -> Футы")
    print("4. Длина: Футы -> Метры")
    print("5. Масса: Килограммы -> Фунты")
    print("6. Масса: Фунты -> Килограммы")
    print("7. Расстояние: Километры -> Мили")
    print("8. Расстояние: Мили -> Километры")
    print("9. Объем: Литры -> Галлоны")
    print("10. Объем: Галлоны -> Литры")
    print("0. Выход")


def get_user_input():
    """
    Получает выбор пользователя и значение для конвертации

    Returns:
        tuple: (выбор_меню, значение_для_конвертации)
    """
    try:
        choice = int(input("Выберите тип конвертации (0-10): "))
        if choice == 0:
            return 0, 0

        value = float(input("Введите значение для конвертации: "))
        return choice, value
    except ValueError:
        print("Ошибка: Введите корректное числовое значение")
        return None, None


def perform_conversion(choice, value):
    """
    Выполняет конвертацию на основе выбора пользователя

    Args:
        choice (int): Выбор из меню
        value (float): Значение для конвертации

    Returns:
        tuple: (результат, описание)
    """
    conversions = {
        1: (celsius_to_fahrenheit, "°C", "°F"),
        2: (fahrenheit_to_celsius, "°F", "°C"),
        3: (meters_to_feet, "м", "футов"),
        4: (feet_to_meters, "футов", "м"),
        5: (kilograms_to_pounds, "кг", "фунтов"),
        6: (pounds_to_kilograms, "фунтов", "кг"),
        7: (kilometers_to_miles, "км", "миль"),
        8: (miles_to_kilometers, "миль", "км"),
        9: (liters_to_gallons, "литров", "галлонов"),
        10: (gallons_to_liters, "галлонов", "литров")
    }

    if choice in conversions:
        func, from_unit, to_unit = conversions[choice]
        result = func(value)
        description = f"{value} {from_unit} = {result:.2f} {to_unit}"
        return result, description
    else:
        return None, "Неверный выбор"


def main():
    """Основная функция для запуска конвертера"""
    print("Добро пожаловать в конвертер единиц измерения!")

    while True:
        display_conversion_menu()
        choice, value = get_user_input()

        if choice == 0:
            print("Выход из программы. До свидания!")
            break

        if choice is None:
            continue

        result, description = perform_conversion(choice, value)

        if result is not None:
            print(f"Результат: {description}")
        else:
            print("Ошибка: Неверный выбор конвертации")

        input("Нажмите Enter для продолжения...")


if __name__ == "__main__":
    main()