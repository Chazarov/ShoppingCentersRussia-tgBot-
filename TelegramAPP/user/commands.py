from aiogram import F, types, Router
from aiogram.filters import Command

from TelegramAPP.user.kbds import reply
from TelegramAPP.user.blanks import MESSAGES

user_commands_router = Router()

@user_commands_router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(MESSAGES["hello"], reply_markup = reply.start_kb)

@user_commands_router.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(MESSAGES["help"])

