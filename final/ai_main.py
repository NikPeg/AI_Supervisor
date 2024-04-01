from aiogram import executor

import config
import messages
from loader import bot, dp
from utils.bot_start_func.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await bot.send_message(config.ADMIN_ID, messages.BOT_STARTED)
    await set_default_commands(dispatcher)
    # asyncio.create_task(start_feed_back())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
