from aiogram.types import BotCommand


user_commands = [
    BotCommand(command='start', description='начать работу с ботом'),
    BotCommand(command='help', description='инструкция по работе с ботом'),
    BotCommand(command='find_in_city', description='найти тц в выбранном городе'),
    BotCommand(command='find_by_name', description='Найти тц по названию'),
]

MESSAGES = {
    "hello": """Привет! Этот бот содержит базу всех торговых центров России. Набери команду /find_by_name чтобы найти центр по названию. 
    Или команду /find_in_city чтобы найти центры в выбранном городе.""",
    "help": """ Набери команду /find_by_name чтобы найти центр по названию. 
    Или команду /find_in_city чтобы нйти центры в выбранном городе. """
}