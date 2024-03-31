import asyncio
import logging

from aiogram import executor

from constants import messages
from database import *
from handlers.users.feedback_func import start_feed_back
from utils.bot_start_func.set_bot_commands import set_default_commands
from loader import bot, dp

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    await bot.send_message(config.ADMIN_ID, messages.BOT_STARTED)
    await asyncio.create_task(start_feed_back())
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
