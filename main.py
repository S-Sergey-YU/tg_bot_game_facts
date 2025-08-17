import random
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

# Применяем патч для asyncio в Google Colab
nest_asyncio.apply()

# Ваш токен Telegram-бота
TOKEN = "8292758536:AAFI_jKjtUYU3rbRWjCnwnIeQcEKkTB-XHM"

# Возможные варианты выборов
CHOICES = ['камень', 'ножницы', 'бумага']

# Список интересных фактов
FUN_FACTS = [
    "Самое длинное слово в русском языке состоит из 35 букв.",
    "Средняя продолжительность жизни кошки около 15 лет.",
    "Первым официальным языком программирования стал Fortran.",
    "Самая высокая гора на Земле — Эверест высотой 8848 метров над уровнем моря.",
    "Первая фотография была сделана Жозефом Нисефором Ньепсом в 1826 году.",
    "Самый большой динозавр, найденный учёными, — аргентинозавр длиной около 35 метров!",
    "Сердце синего кита весит примерно столько же, сколько маленький автомобиль.",
    "Кошачьи отпечатки лап уникальны, как человеческие отпечатки пальцев!"
]

# Стартовая страница бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Играть в Камень-Ножницы-Бумагу", callback_data='play_game')],
        [InlineKeyboardButton("Получить интересный факт", callback_data='fun_fact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать! Выберите действие:", reply_markup=reply_markup)

# Получение случайного факта
async def fun_facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fact = random.choice(FUN_FACTS)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(f"Интересный факт: {fact}")

# Игра "Камень-Ножницы-Бумага": показ вариантов выбора
async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choices_buttons = [[InlineKeyboardButton(choice.capitalize(), callback_data=f'choice_{choice}')] for choice in CHOICES]
    reply_markup = InlineKeyboardMarkup(choices_buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Ваш ход:", reply_markup=reply_markup)

# Логика определения победителя
def determine_winner(user_choice, bot_choice):
    winner_map = {
        ('камень', 'ножницы'): True,
        ('ножницы', 'бумага'): True,
        ('бумага', 'камень'): True
    }
    if user_choice == bot_choice:
        return "Ничья"
    elif winner_map.get((user_choice, bot_choice)):
        return "Вы победили!"
    else:
        return "Вы проиграли :("

# Показ результата игры
async def game_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.callback_query.data.split('_')[1]
    
    # Генерируем выбор бота только один раз
    bot_choice = random.choice(CHOICES)
    
    # Определяем победителя
    result = determine_winner(user_choice, bot_choice)
    
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(f"Ваш выбор: {user_choice}\nВыбор бота: {bot_choice}\nРезультат: {result}")

    # Переход назад в главное меню
    keyboard = [
        [InlineKeyboardButton("Играть ещё раз", callback_data='play_game')],
        [InlineKeyboardButton("Ещё один интересный факт", callback_data='fun_fact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Продолжим?", reply_markup=reply_markup)

# Основной блок запуска приложения
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков команд и кликов
    application.add_handler(CallbackQueryHandler(fun_facts, pattern='^fun_fact$'))
    application.add_handler(CallbackQueryHandler(play_game, pattern='^play_game$'))
    application.add_handler(CallbackQueryHandler(game_result, pattern='^choice_'))
    application.add_handler(CommandHandler('start', start))

    # Запуск бота
    application.run_polling()
