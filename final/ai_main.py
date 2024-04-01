import asyncio
import logging

from aiogram import executor

from handlers.users.feedback_func import start_feed_back
from loader import dp
from utils.bot_start_func.set_bot_commands import set_default_commands

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    task1 = set_default_commands(dispatcher)
    task = asyncio.create_task(start_feed_back())
    await asyncio.gather(task1, task)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
