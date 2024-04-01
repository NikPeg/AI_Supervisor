import logging

from aiogram import executor

import messages
from utils.bot_start_func.set_bot_commands import set_default_commands

logging.basicConfig(level=logging.INFO)

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(dispatcher):
    await bot.send_message(config.ADMIN_ID, messages.BOT_STARTED)
    await set_default_commands(dispatcher)
    # asyncio.create_task(start_feed_back())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
