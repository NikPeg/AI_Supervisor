import asyncio
from aiogram import executor
from loader import dp,bot
from utils.bot_start_func.set_bot_commands import set_default_commands
import logging
from handlers.users.feedback_func import start_feed_back
import handlers

logging.basicConfig(level=logging.INFO)





async def on_startup(dispatcher):
    asyncio.create_task(start_feed_back())
    await set_default_commands(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup,skip_updates=True)
