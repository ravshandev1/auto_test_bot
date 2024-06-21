import asyncio
import logging
import sys
from aiogram import Dispatcher, types
from config import ADMIN, bot
from handlers import router

dp: Dispatcher = Dispatcher()


async def bot_stopped():
    await bot.send_message(ADMIN, 'Bot stopped')


async def bot_started():
    await bot.send_message(ADMIN, "Bot started")


async def start():
    dp.startup.register(bot_started)
    dp.shutdown.register(bot_stopped)
    dp.include_router(router)
    await bot.set_my_commands([types.BotCommand(command='start', description='Start the bot.')])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
