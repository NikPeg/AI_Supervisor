import asyncio

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import ADMIN_ID
from constants import buttons, messages
from database.mess_db import add_new_message
from database.sessia_db import create_new_sessia
from database.users_db import add_new_user
from gpt_func import gpt_ask_func
from keyboards.keyboards import start_markup, return_markup
from ... import bot, dp


class UserState(StatesGroup):
    gpt_req = State()
    feedback = State()


@dp.message_handler(commands=['start'], state="*")
async def start_command_handler(message: types.Message):
    add_new_user(message.chat.id, message.chat.username)
    await bot.send_message(message.chat.id, messages.START, reply_markup=start_markup())
    create_new_sessia(message.chat.id)
    await bot.send_message(message.chat.id, messages.PROMPT)
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(message.chat.id, message.chat.username, message.text)
    )
    await UserState.gpt_req.set()


@dp.callback_query_handler(text='info', state="*")
async def info_handler(call: types.CallbackQuery):
    await call.message.edit_text(messages.HELP, reply_markup=return_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, buttons.ABOUT.text),
    )


@dp.callback_query_handler(text='return', state="*")
async def return_handler(call: types.CallbackQuery):
    await call.message.edit_text(messages.START, reply_markup=start_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, buttons.BACK.text),
    )


@dp.message_handler(commands=['help'], state="*")
async def help_message_handler(message: types.Message):
    await bot.send_message(message.chat.id, messages.HELP)
    await bot.send_message(message.chat.id, messages.PROMPT)
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(message.chat.id, message.chat.username, message.text),
    )


@dp.message_handler(commands=['new'], state="*")
async def help_message_handler(message: types.Message):
    await bot.send_message(message.chat.id, messages.NEW_CASE)
    create_new_sessia(message.chat.id)
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(message.chat.id, message.chat.username, message.text),
    )
    await UserState.gpt_req.set()


@dp.message_handler(state=UserState.gpt_req)
async def user_gpt_req_handler(message: types.Message):
    req_text = message.text
    await asyncio.create_task(create_user_req(message.chat.id, message.chat.username, req_text))


async def create_user_req(user_id, user_name, req_text):
    bot_req = gpt_ask_func(req_text)
    add_new_message(user_id, req_text, bot_req)
    await bot.send_message(user_id, bot_req)
    await bot.send_message(
        ADMIN_ID,
        messages.SENT.format(user_id, user_name, req_text, bot_req),
    )
