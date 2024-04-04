import asyncio

import openai
from aiogram import types
from config import ADMIN_ID

import messages
from handlers.common import create_user_req
from loader import dp, bot


@dp.message_handler(commands=['answer'], state="*")
async def help_message_handler(message: types.Message):
    if not message.reply_to_message:
        bot.send_message(ADMIN_ID, messages.WRONG_MESSAGE)
        return
    user_id = int(message.reply_to_message.text.split()[1])
    username = message.reply_to_message.text.split()[4][1:]
    request_text = message.reply_to_message.text
    try:
        await asyncio.create_task(create_user_req(user_id, username, request_text))
    except openai.BadRequestError as e:
        await bot.send_message(message.chat.id, messages.WAIT)
        await bot.send_message(ADMIN_ID, messages.WAIT + e)
    except Exception as e:
        await bot.send_message(ADMIN_ID, messages.UNKNOWN_ERROR + e)
