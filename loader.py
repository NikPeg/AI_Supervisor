from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from cloudpayments import CloudPayments

import config
from gpt.proxy import GPTProxy

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
gpt = GPTProxy(config.GPT_TOKEN, config.MODEL, bot)
client = CloudPayments(config.PAYMENTS_ID, config.PAYMENTS_TOKEN)
