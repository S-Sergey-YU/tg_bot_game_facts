import random
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters

# Применение patch для asyncio в Google Colab
nest_asyncio.apply()

# Токен вашего Telegram-бота
TOKEN = "Your_token"

# Возможные выборы в игре
CHOICES = ['камень', 'ножницы', 'бумага']

# Интересные факты
FUN_FACTS = [
    "Самое длинное слово в русском языке состоит из 35 букв.",
    "Средняя продолжительность жизни кошки около 15 лет.",
    "Первым официальным языком программирования стал Fortran.",
    "Самая высокая гора на Земле — Эверест высотой 8848 метров над уровнем моря.",
    "Первая фотография сделана Жозефом Нисефором Ньепсом в 1826 году."
]

# Главная страница бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Поиграть в Камень-Ножницы-Бумага", callback_data='play_game')],
        [InlineKeyboardButton("Узнать интересные факты", callback_data='fun_fact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать! Выберите, что хотите сделать.", reply_markup=reply_markup)

# Лента интересных фактов
async def fun_facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fact = random.choice(FUN_FACTS)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(f"Интересный факт: {fact}")

# Основная игра "Камень-Ножницы-Бумага"
async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choices_buttons = [[InlineKeyboardButton(choice.capitalize(), callback_data=f'choice_{choice}')] for choice in CHOICES]
    reply_markup = InlineKeyboardMarkup(choices_buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Сделайте ваш выбор:", reply_markup=reply_markup)

# Определяем победителя в игре
def determine_winner(user_choice):
    bot_choice = random.choice(CHOICES)
    winner_map = {
        ('камень', 'ножницы'): True,
        ('ножницы', 'бумага'): True,
        ('бумага', 'камень'): True
    }
    if user_choice == bot_choice:
        return "ничья"
    elif winner_map.get((user_choice, bot_choice)):
        return "победа"
    else:
        return "поражение"

# Результат игры и возврат в меню
async def game_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.callback_query.data.split('_')[1]
    result = determine_winner(user_choice)
    bot_choice = random.choice(CHOICES)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(f"Ваш выбор: {user_choice}.\nВыбор бота: {bot_choice}.\nРезультат: {result}.")

    # Возвращаемся в главное меню
    keyboard = [
        [InlineKeyboardButton("Поиграть в Камень-Ножницы-Бумага", callback_data='play_game')],
        [InlineKeyboardButton("Узнать интересные факты", callback_data='fun_fact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Хотите повторить или попробовать другое?", reply_markup=reply_markup)

# Коллектор событий
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    # Настройки кнопок
    application.add_handler(CallbackQueryHandler(fun_facts, pattern='^fun_fact$'))
    application.add_handler(CallbackQueryHandler(play_game, pattern='^play_game$'))
    application.add_handler(CallbackQueryHandler(game_result, pattern='^choice_'))

    # Первая команда
    application.add_handler(CommandHandler("start", start))

    # Запуск бота
    application.run_polling()