import asyncio
import os

from aiogram import Bot, Dispatcher, types

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from Database.engine import as_create_db, session_maker
from TelegramAPP.middlewares.db import DataBaseSession
from TelegramAPP.user.commands import user_commands_router
from TelegramAPP.user.dialogues import user_dialogues_router
from TelegramAPP.user.blanks import user_commands


bot = Bot(token = os.getenv("TOKEN"))

dp = Dispatcher()

dp.include_router(user_commands_router)
dp.include_router(user_dialogues_router)


async def on_startup(bot):
    await as_create_db()

async def on_shutdown(bot):
    print("бот лег")

async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool = session_maker))

    await bot.delete_webhook(drop_pending_updates = True)
    await bot.set_my_commands(commands = user_commands,scope = types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
