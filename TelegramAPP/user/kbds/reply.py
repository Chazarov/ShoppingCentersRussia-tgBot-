from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_kb = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "Поиск по названию"),
            KeyboardButton(text = "Поиск в городе"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?",
)

del_kbd = ReplyKeyboardRemove()

