import asyncio

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

import messages
from config import ADMIN_ID
from database.message_db import add_new_message, get_conversation_by_user
from database.session_db import create_new_session, get_user_session_id
from database.user_db import add_new_user
from keyboards.keyboards import start_markup, return_markup
from loader import dp, bot, gpt
from messages import HELP, START, PROMPT, NEW_PROMPT


class UserState(StatesGroup):
    gpt_req = State()
    feedback = State()


@dp.message_handler(commands=['start'], state="*")
async def start_command_handler(message: types.Message):
    add_new_user(message.chat.id, message.chat.username)
    await bot.send_message(message.chat.id, START, reply_markup=start_markup())
    create_new_session(message.chat.id)
    await bot.send_message(message.chat.id, PROMPT)
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(message.chat.id, message.chat.username, message.text),
    )
    await UserState.gpt_req.set()


@dp.callback_query_handler(text='info', state="*")
async def info_handler(call: types.CallbackQuery):
    await call.message.edit_text(HELP, reply_markup=return_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, "ℹ️Узнать о frAId"),
    )


@dp.callback_query_handler(text='return', state="*")
async def return_handler(call: types.CallbackQuery):
    await call.message.edit_text(START, reply_markup=start_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, "Назад"),
    )


@dp.message_handler(commands=['help'], state="*")
async def help_message_handler(message: types.Message):
    await bot.send_message(message.chat.id, HELP)
    await bot.send_message(message.chat.id, PROMPT)
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(message.chat.id, message.chat.username, message.text),
    )


@dp.message_handler(commands=['new'], state="*")
async def help_message_handler(message: types.Message):
    await bot.send_message(message.chat.id, NEW_PROMPT)
    create_new_session(message.chat.id)
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(message.chat.id, message.chat.username, message.text),
    )
    await UserState.gpt_req.set()


@dp.message_handler(state=UserState.gpt_req)
async def user_gpt_req_handler(message: types.Message):
    req_text = message.text
    await asyncio.create_task(create_user_req(message.chat.id, message.chat.username, req_text))


async def create_user_req(user_id, user_name, request_text):
    conversation = get_conversation_by_user(user_id)
    bot_req = gpt.ask(request_text)
    add_new_message(user_id, request_text, bot_req)
    await bot.send_message(user_id, bot_req)
    await bot.send_message(
        ADMIN_ID,
        messages.MESSAGE_SENT.format(user_id, user_name, request_text, bot_req),
    )
