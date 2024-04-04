import asyncio

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from config import ADMIN_ID

import buttons
import messages
from database.message_db import add_new_message
from database.session_db import create_new_session, get_thread_id
from database.user_db import add_new_user
from keyboards.keyboards import start_markup, return_markup
from loader import dp, bot, gpt
from messages import HELP, START, PROMPT, NEW_PROMPT


class UserState(StatesGroup):
    gpt_request = State()
    feedback = State()


@dp.message_handler(commands=['start'], state="*")
async def start_command_handler(message: types.Message):
    add_new_user(message.chat.id, message.chat.username)
    await bot.send_message(message.chat.id, START, reply_markup=start_markup())
    await bot.send_message(message.chat.id, PROMPT)
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(message.chat.id, message.chat.username, message.text),
    )
    await UserState.gpt_request.set()


@dp.callback_query_handler(text='info', state="*")
async def info_handler(call: types.CallbackQuery):
    await call.message.edit_text(HELP, reply_markup=return_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, buttons.ABOUT.text),
    )


@dp.callback_query_handler(text='return', state="*")
async def return_handler(call: types.CallbackQuery):
    await call.message.edit_text(START, reply_markup=start_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, buttons.BACK.text),
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
    await UserState.gpt_request.set()


@dp.message_handler(state=UserState.gpt_request)
@dp.message_handler(state=default_state)
async def user_gpt_req_handler(message: types.Message):
    request_text = message.text
    await asyncio.create_task(create_user_req(message.chat.id, message.chat.username, request_text))


def process_text(text):
    return (
        text
        .replace("\_", "\\_")
        # .replace("\*", "\\*")
        .replace("\[", "\\[")
        .replace("\]", "\\]")
        .replace("\(", "\\(")
        .replace("\)", "\\)")
        .replace("\~", "\\~")
        # .replace("\`", "\\`")
        .replace("\>", "\\>")
        .replace("\#", "\\#")
        .replace("\+", "\\+")
        .replace("\-", "\\-")
        .replace("\=", "\\=")
        .replace("\|", "\\|")
        .replace("\{", "\\{")
        .replace("\}", "\\}")
        .replace("\.", "\\.")
        .replace("\!", "\\!")
    )


async def create_user_req(user_id, user_name, request_text):
    await bot.send_message(
        ADMIN_ID,
        messages.MESSAGE_SENT.format(user_id, user_name, request_text),
    )
    thread_id = get_thread_id(user_id)
    await gpt.add_message(thread_id, request_text)
    bot_answer = await gpt.get_answer(thread_id)
    try:
        await bot.send_message(user_id, bot_answer, parse_mode='Markdown')
    except Exception as e:
        print(e)
        await bot.send_message(user_id, bot_answer)
    await bot.send_message(
        ADMIN_ID,
        messages.BOT_ANSWERED.format(user_id, user_name, bot_answer),
    )
    add_new_message(user_id, request_text, bot_answer)
