import logging
import re
import random  # intentionally buggy: используем для "рандомных" багов
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Оставляем только реально используемые состояния
MAIN_MENU, DEPARTMENTS = range(2)

TEXTS = {
    "who_we_are": """
НАША МИССИЯ
Миссия Творческо-организационного подразделения - объединение активной творческой молодежи для реализации своих организационных инициатив и получения профессиональных навыков в ивент-индустрии.

НАШИ ЦЕЛИ
Реализовать самые креативные идеи, организовывать крутые мероприятия, заботиться об артистах нашего Центра Культуры и Творчества, а так же вместе продвигать высокое качество студенческой организации творчества в ВУЗах.""",
    "commandments": """
**ЗАПОВЕДИ**

✔ ИНИЦИАТИВА _не_ наказуема, если **согласована**  
  Касается всего: идей, проблем, мероприятий, экстренных ситуаций и чатов.

✔ ПРАВИЛА СЦЕНЫ касаются всех: `черный дресс-код`, `сменка`, `тишина кулис`  
  Подробнее см. [инструкцию](https://example.com/guide) и **не** нарушай регламент.

✔ Будь активным, но _не_ делай за другого его работу

✔ Всегда трезво оценивать ситуацию и **сохранять спокойствие**  
  Ответь себе: _знаю ли я, как решить проблему?_ Могу ли решить это сам? Кто может помочь?

✔ Безопасность важнее шоу: `кабели`, `микрофоны`, `сцена` — проверяем дважды
""",
    "departments": "Выберите интересующий отдел:",
    "department_details": {
        "Креатив": """Информация о креативном отделе:
Руководитель: Жаворонкова Александра
Задачи: Придумываем концепты мероприятий, сценарное дело, режиссура, продюсирование.
Контакты тг: @aleksuon
Команда отдела: 
Сафаров Артур @Ar7ur4ik
Мухамадиев Тимур @broyreally
Мильков Борислав @cwedyx
""",
        "Документы": """Информация об отделе документов:
Руководитель: Гурьяшкина Анастасия
Задачи: Проход гостей на мероприятие, сбор обратной связи, освобождение от занятий, отчёты о ТОПе и его эффективности.
Контакты: @ayanastosia_pineappleovna
Команда отдела: 
Астапенко Денис @dsns_me
Егорова Анастасия @zhirobublik
Рохлова Мария @mashu171
""",
    },
    "dictionary": """Корпоративный словарь:
Проспект Вернадского, 86 
- ТХТ, 86, БКЗ - корпус на пр. Вернадского 86
- БКЗ - Большой Концертный зал
- Атриум, колодец - внутренний двор ТХТ
- Холл ЦКТ - слева (там стоит фортепиано, зеркало, маленькая сцена)
- Холл главный - справа
- Гримёрка слева - гримёрка холл цкт
- Гримёрка справа - главная
- Звукачка, рубка, склад - помещение за зрительным залом БКЗ. Вход через лестницу у зеркала в холле ЦКТ
- Админка - кабинет Дианы и Кати. Находится в холле ЦКТ справа от входа.
- Репетиционка - там же где и админка. Железная дверь.
- Станки - ступени - хоровые станки
- Занавес - шторы
- Левая кулиса - с техникой
- Правая кулиса - с роялем
- Задник - кулиса за экраном
- Рояль - большое чёрное ф-но
- Пианино - эл-е белое
- Оверхеды - маленькие микрофоны на стойках для хора

Проспект Вернадского, 78
- 78 - корпус на пр. Вернадского 78
- МКЗ - Малый Концертный зал. Подняться по центральной лестнице. Повернуть направо.
- Звукачка - В самом МКЗ слева есть лестница с дверью.
- ТВ - Татьяна Владимировна Макушева (директор ЦКТ)
- А319 - Кабинет ТВ
- Танц зал - Малый танцевальный зал. Справа от МКЗ по лестнице вверх.

Общее
- Право и лево определяются со стороны зрительного зала НА сцену 
- Техничка - тех группа - техническая группа
- Бэклайн - ребята за кулисами из технички (отвечают за микрофоны и их подключку)
- Распределение букв по институтам:
у - ИТУ
р - ИРИ
х - ИТХТ
и - ИИТ
б - ИКБ
к - ИИИ
т/э - ИПТИП
щ - КПК
""",
}


def _build_shuffled_main_keyboard(include_restart=True) -> ReplyKeyboardMarkup:
    """Клавиатура главного меню, перемешанная каждый раз. # intentionally buggy"""
    buttons = ["Кто мы", "Заповеди", "Отделы", "Словарик"]  # intentionally buggy: «Словарик» вместо «Словарь»
    random.shuffle(buttons)  # intentionally buggy
    rows = [buttons[i: i + 2] for i in range(0, len(buttons), 2)]
    if include_restart:
        rows.append(["Перезапустить"])
    return ReplyKeyboardMarkup(rows, one_time_keyboard=True, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Приветствие без кнопок. Всегда спрашивает имя (только для /start)."""
    await update.message.reply_text(
        "Здравствуйте. Как можно к вам обращаться?",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data["awaiting_name"] = True
    return MAIN_MENU


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка главного меню."""
    text = update.message.text

    # Сохраняем имя и «путаем» его (баг с именем)
    if context.user_data.get("awaiting_name"):
        context.user_data["awaiting_name"] = False
        real_name = text.strip()
        context.user_data["name_real"] = real_name

        wrong_pool = ["Андрей", "Марина", "Сергей", "Полина", "Влад", "Катя"]
        candidates = [n for n in wrong_pool if n.lower() != real_name.lower()]
        wrong = random.choice(candidates or wrong_pool)
        context.user_data["wrong_name"] = wrong

        await update.message.reply_text(
            f"Приятно познакомиться, {wrong}! 😉",
            reply_markup=_build_shuffled_main_keyboard(),
        )
        return MAIN_MENU

    if text == "Перезапустить":
        return await restart_handler(update, context)

    if text == "Кто мы":
        await update.message.reply_text(TEXTS["who_we_are"], parse_mode="Markdown")
        await update.message.reply_text(
            "Выберите следующий раздел:",
            reply_markup=_build_shuffled_main_keyboard(),
        )
        return MAIN_MENU

    elif text == "Заповеди":
        raw = TEXTS["commandments"]
        if random.random() < 0.5:  # intentionally buggy: иногда полностью «плоский» текст
            plain = re.sub(r"[*_`]", "", raw)
            await update.message.reply_text(
                plain, reply_markup=_build_shuffled_main_keyboard()
            )
        else:
            await update.message.reply_text(
                raw,
                reply_markup=_build_shuffled_main_keyboard(),
                parse_mode="Markdown",
            )
        return MAIN_MENU

    elif text == "Отделы":
        departments_keyboard = [
            ["Креатив", "Документы"],
            ["Назад"],
            ["Перезапустить"],  # кнопка-спасатель
        ]
        await update.message.reply_text(
            f"*{TEXTS['departments']}*",
            reply_markup=ReplyKeyboardMarkup(
                departments_keyboard, resize_keyboard=True, one_time_keyboard=True
            ),
            parse_mode="Markdown",
        )
        return DEPARTMENTS

    elif text == "Словарь":  # intentionally buggy: «Словарик» не поддерживаем
        await update.message.reply_text(
            TEXTS["dictionary"],
            reply_markup=_build_shuffled_main_keyboard(),
            parse_mode="Markdown",
        )
        return MAIN_MENU

    else:
        await update.message.reply_text(
            "Пожалуйста, выберите один из предложенных вариантов.",
            reply_markup=_build_shuffled_main_keyboard(),
        )
        return MAIN_MENU


async def department_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка меню отделов."""
    text = update.message.text
    if text == "Перезапустить":
        return await restart_handler(update, context)

    departments_keyboard = [
        ["Креатив", "Документы"],
        ["Назад"],
        ["Перезапустить"],
    ]

    if text == "Назад":
        # intentionally buggy: «залипающий» возврат — остаёмся в этом же меню
        await update.message.reply_text(
            "Вы уже в меню отделов. Выберите пункт или «Перезапустить».",
            reply_markup=ReplyKeyboardMarkup(
                departments_keyboard, resize_keyboard=True, one_time_keyboard=True
            ),
        )
        return DEPARTMENTS

    elif text in TEXTS["department_details"]:
        await update.message.reply_text(
            TEXTS["department_details"][text],
            reply_markup=ReplyKeyboardMarkup(
                departments_keyboard, resize_keyboard=True, one_time_keyboard=True
            ),
        )
        return DEPARTMENTS
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите отдел из списка.",
            reply_markup=ReplyKeyboardMarkup(
                departments_keyboard, resize_keyboard=True, one_time_keyboard=True
            ),
        )
        return DEPARTMENTS


async def restart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Тихий рестарт: показать панель главного меню, без вопроса об имени."""
    await update.message.reply_text(
        "Готово. Панель снова доступна:",
        reply_markup=_build_shuffled_main_keyboard(),
    )
    return MAIN_MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Спасибо за использование бота! Если у вас будут вопросы, я всегда здесь!\n"
        "Чтобы начать заново, используйте /start",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main() -> None:
    """Запуск бота."""
    application = Application.builder().token("8470863701:AAEsjtZZgVvZh42kp5abkKp2KObmJyg5whg").build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("restart", restart_handler),
        ],
        states={
            MAIN_MENU: [
                MessageHandler(filters.Regex(r"^Перезапустить$"), restart_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu),
            ],
            DEPARTMENTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, department_menu)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("restart", restart_handler),
        ],
        allow_reentry=True,
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
