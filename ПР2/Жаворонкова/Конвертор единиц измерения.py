import tkinter as tk
from tkinter import ttk, messagebox


class UnitConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📐 Конвертер единиц измерения")
        self.root.geometry("450x350")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f8ff')

        # Стили для виджетов
        self.setup_styles()

        # Переменные
        self.input_value = tk.StringVar(value="0")
        self.output_value = tk.StringVar(value="0")
        self.conversion_type = tk.StringVar(value="temperature")
        self.from_unit = tk.StringVar()
        self.to_unit = tk.StringVar()

        self.setup_ui()
        self.update_unit_choices()

    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')

        # Настройка стилей
        style.configure('TFrame', background='#f0f8ff')
        style.configure('TLabel', background='#f0f8ff', font=('Arial', 10))
        style.configure('Title.TLabel', background='#f0f8ff', font=('Arial', 12, 'bold'))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Convert.TButton', background='#4CAF50', foreground='white')
        style.configure('Clear.TButton', background='#f44336', foreground='white')
        style.configure('TCombobox', font=('Arial', 9))
        style.configure('TEntry', font=('Arial', 10))

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Главный заголовок
        title_label = ttk.Label(self.root, text="🔄 КОНВЕРТЕР ЕДИНИЦ ИЗМЕРЕНИЯ", style='Title.TLabel')
        title_label.pack(pady=10)

        # Основной контейнер
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(padx=20, pady=10, fill='both', expand=True)

        # Сетка для компактного расположения
        row = 0

        # Тип конвертации
        ttk.Label(main_frame, text="Тип конвертации:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=8)
        conversion_types = ttk.Combobox(main_frame, textvariable=self.conversion_type,
                                        values=["temperature", "length", "mass", "volume"],
                                        width=20, state="readonly")
        conversion_types.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=8)
        conversion_types.bind('<<ComboboxSelected>>', self.update_unit_choices)
        row += 1

        # Ввод значения
        ttk.Label(main_frame, text="Введите значение:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=8)
        input_entry = ttk.Entry(main_frame, textvariable=self.input_value, width=23, font=('Arial', 11))
        input_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=8)
        input_entry.select_range(0, tk.END)
        input_entry.focus()
        row += 1

        # Единицы измерения в одной строке
        units_frame = ttk.Frame(main_frame, style='TFrame')
        units_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=8)

        ttk.Label(units_frame, text="Из:").pack(side=tk.LEFT, padx=(0, 5))
        self.from_combo = ttk.Combobox(units_frame, textvariable=self.from_unit, width=15, state="readonly")
        self.from_combo.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(units_frame, text="в").pack(side=tk.LEFT, padx=5)

        ttk.Label(units_frame, text="В:").pack(side=tk.LEFT, padx=(20, 5))
        self.to_combo = ttk.Combobox(units_frame, textvariable=self.to_unit, width=15, state="readonly")
        self.to_combo.pack(side=tk.LEFT)
        row += 1

        # Кнопки
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.grid(row=row, column=0, columnspan=2, pady=15)

        convert_btn = ttk.Button(button_frame, text="🔄 Конвертировать",
                                 command=self.convert, style='Convert.TButton')
        convert_btn.pack(side=tk.LEFT, padx=10)

        clear_btn = ttk.Button(button_frame, text="🧹 Очистить",
                               command=self.clear, style='Clear.TButton')
        clear_btn.pack(side=tk.LEFT, padx=10)
        row += 1

        # Результат
        result_frame = ttk.Frame(main_frame, style='TFrame')
        result_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=10)

        ttk.Label(result_frame, text="Результат:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        result_entry = ttk.Entry(result_frame, textvariable=self.output_value,
                                 state="readonly", font=('Arial', 11, 'bold'),
                                 foreground='#2E7D32', width=20)
        result_entry.pack(side=tk.RIGHT, padx=(10, 0))

        # Разделитель
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=row + 1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=15)

        # Подсказка
        hint_label = ttk.Label(main_frame,
                               text="💡 Подсказка: Выберите тип конвертации и единицы измерения, затем введите значение",
                               font=('Arial', 8), foreground='#666666')
        hint_label.grid(row=row + 2, column=0, columnspan=2, pady=5)

    def get_russian_unit_names(self, conversion_type):
        """Возвращает русские названия единиц измерения"""
        units = {
            "temperature": ["Цельсий", "Фаренгейт", "Кельвин"],
            "length": ["Метры", "Километры", "Мили", "Футы", "Дюймы"],
            "mass": ["Килограммы", "Граммы", "Фунты", "Унции"],
            "volume": ["Литры", "Миллилитры", "Галлоны", "Кубические метры"]
        }
        return units.get(conversion_type, [])

    def update_unit_choices(self, event=None):
        """Обновляет доступные единицы измерения в зависимости от типа конвертации"""
        conversion_type = self.conversion_type.get()

        # Русские названия для отображения
        display_units = self.get_russian_unit_names(conversion_type)

        # Английские названия для внутренней логики
        internal_units = {
            "temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "length": ["Meters", "Kilometers", "Miles", "Feet", "Inches"],
            "mass": ["Kilograms", "Grams", "Pounds", "Ounces"],
            "volume": ["Liters", "Milliliters", "Gallons", "Cubic Meters"]
        }

        self.from_combo['values'] = display_units
        self.to_combo['values'] = display_units

        if display_units:
            self.from_unit.set(display_units[0])
            self.to_unit.set(display_units[1] if len(display_units) > 1 else display_units[0])

    def get_internal_unit_name(self, russian_name):
        """Преобразует русское название единицы во внутреннее английское"""
        mapping = {
            "Цельсий": "Celsius", "Фаренгейт": "Fahrenheit", "Кельвин": "Kelvin",
            "Метры": "Meters", "Километры": "Kilometers", "Мили": "Miles",
            "Футы": "Feet", "Дюймы": "Inches",
            "Килограммы": "Kilograms", "Граммы": "Grams", "Фунты": "Pounds", "Унции": "Ounces",
            "Литры": "Liters", "Миллилитры": "Milliliters", "Галлоны": "Gallons",
            "Кубические метры": "Cubic Meters"
        }
        return mapping.get(russian_name, russian_name)

    def celsius_to_fahrenheit(self, celsius):
        """Конвертирует Цельсии в Фаренгейты"""
        return (celsius * 9 / 5) + 32

    def fahrenheit_to_celsius(self, fahrenheit):
        """Конвертирует Фаренгейты в Цельсии"""
        return (fahrenheit - 32) * 5 / 9

    def celsius_to_kelvin(self, celsius):
        """Конвертирует Цельсии в Кельвины"""
        return celsius + 273.15

    def kelvin_to_celsius(self, kelvin):
        """Конвертирует Кельвины в Цельсии"""
        return kelvin - 273.15

    def convert_temperature(self, value, from_unit, to_unit):
        """Конвертирует температуру между различными единицами"""
        conversions = {
            ("Celsius", "Fahrenheit"): self.celsius_to_fahrenheit,
            ("Fahrenheit", "Celsius"): self.fahrenheit_to_celsius,
            ("Celsius", "Kelvin"): self.celsius_to_kelvin,
            ("Kelvin", "Celsius"): self.kelvin_to_celsius,
            ("Fahrenheit", "Kelvin"): lambda x: self.celsius_to_kelvin(self.fahrenheit_to_celsius(x)),
            ("Kelvin", "Fahrenheit"): lambda x: self.celsius_to_fahrenheit(self.kelvin_to_celsius(x))
        }

        if from_unit == to_unit:
            return value

        converter = conversions.get((from_unit, to_unit))
        if converter:
            return converter(value)
        else:
            # ПРЕДНАМЕРЕННАЯ ОШИБКА: неправильная формула для Kelvin to Fahrenheit
            if from_unit == "Kelvin" and to_unit == "Fahrenheit":
                return (value - 273.15) * 1.8 + 35  # Должно быть +32, а не +35

            raise ValueError(f"Конвертация из {from_unit} в {to_unit} не поддерживается")

    def convert_length(self, value, from_unit, to_unit):
        """Конвертирует длину между различными единицами"""
        # Конвертируем в метры
        to_meters = {
            "Meters": 1,
            "Kilometers": 1000,
            "Miles": 1609.344,
            "Feet": 0.3048,
            "Inches": 0.0254
        }

        # Конвертируем из метров в целевую единицу
        from_meters = {unit: 1 / factor for unit, factor in to_meters.items()}

        if from_unit not in to_meters or to_unit not in to_meters:
            raise ValueError("Неизвестная единица измерения длины")

        meters = value * to_meters[from_unit]
        return meters * from_meters[to_unit]

    def convert_mass(self, value, from_unit, to_unit):
        """Конвертирует массу между различными единицами"""
        # Конвертируем в килограммы
        to_kg = {
            "Kilograms": 1,
            "Grams": 0.001,
            "Pounds": 0.453592,
            "Ounces": 0.0283495
        }

        # Конвертируем из килограммов в целевую единицу
        from_kg = {unit: 1 / factor for unit, factor in to_kg.items()}

        if from_unit not in to_kg or to_unit not in to_kg:
            raise ValueError("Неизвестная единица измерения массы")

        kg = value * to_kg[from_unit]
        return kg * from_kg[to_unit]

    def convert_volume(self, value, from_unit, to_unit):
        """Конвертирует объем между различными единицами"""
        # Конвертируем в литры
        to_liters = {
            "Liters": 1,
            "Milliliters": 0.001,
            "Gallons": 3.78541,
            "Cubic Meters": 1000
        }

        # Конвертируем из литров в целевую единицу
        from_liters = {unit: 1 / factor for unit, factor in to_liters.items()}

        if from_unit not in to_liters or to_unit not in to_liters:
            raise ValueError("Неизвестная единица измерения объема")

        liters = value * to_liters[from_unit]
        return liters * from_liters[to_unit]

    def convert(self):
        """Основная функция конвертации"""
        try:
            value = float(self.input_value.get())
            from_unit_ru = self.from_unit.get()
            to_unit_ru = self.to_unit.get()
            conversion_type = self.conversion_type.get()

            if not from_unit_ru or not to_unit_ru:
                messagebox.showerror("Ошибка", "Выберите единицы измерения")
                return

            # Конвертируем русские названия в английские для внутренней логики
            from_unit = self.get_internal_unit_name(from_unit_ru)
            to_unit = self.get_internal_unit_name(to_unit_ru)

            result = 0

            if conversion_type == "temperature":
                result = self.convert_temperature(value, from_unit, to_unit)
            elif conversion_type == "length":
                result = self.convert_length(value, from_unit, to_unit)
            elif conversion_type == "mass":
                result = self.convert_mass(value, from_unit, to_unit)
            elif conversion_type == "volume":
                result = self.convert_volume(value, from_unit, to_unit)
            else:
                messagebox.showerror("Ошибка", "Неизвестный тип конвертации")
                return

            self.output_value.set(f"{result:.6f}")

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка конвертации: {str(e)}")

    def clear(self):
        """Очищает поля ввода и вывода"""
        self.input_value.set("0")
        self.output_value.set("0")
        # Устанавливаем фокус на поле ввода
        self.root.focus_set()
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Entry) and child.cget('state') != 'readonly':
                        child.focus()
                        child.select_range(0, tk.END)
                        break

    def run(self):
        """Запускает приложение"""
        self.root.mainloop()


if __name__ == "__main__":
    # Запуск с GUI
    app = UnitConverter()
    app.run()