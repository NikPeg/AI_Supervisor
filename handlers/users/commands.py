import asyncio

import openai
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from cloudpayments import Currency

import config
from config import ADMIN_ID

import buttons
import messages
from database.payment_db import check_payment
from database.session_db import create_new_session
from database.user_db import add_new_user
from handlers.common import create_user_req
from keyboards.keyboards import start_markup, return_markup, payment_markup
from loader import dp, bot, client
from messages import HELP, START, PROMPT, NEW_PROMPT


class UserState(StatesGroup):
    gpt_request = State()
    feedback = State()
    payment = State()


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


@dp.callback_query_handler(text='payment', state="*")
async def payment_handler(call: types.CallbackQuery):
    link = client.create_order(config.PRICE, Currency.RUB, messages.PAYMENT_DESCRIPTION, account_id=call.message.chat.id).url
    await call.message.edit_text(messages.PAYMENT_LINK.format(link), reply_markup=return_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, buttons.PAYMENT.text),
    )
    await UserState.payment.set()


@dp.message_handler(state=UserState.payment)
async def paid_handler(message: types.Message):
    await bot.send_message(message.chat.id, messages.PAYMENT_PROCESS, reply_markup=return_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.MESSAGE_SENT.format(message.chat.id, message.chat.username, message.text),
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


@dp.message_handler(commands=['answer'], state="*")
async def answer_message_handler(message: types.Message):
    if message.chat.id != ADMIN_ID:
        return
    if not message.reply_to_message:
        await bot.send_message(ADMIN_ID, messages.WRONG_MESSAGE)
        return
    user_id = int(message.reply_to_message.text.split()[1])
    username = message.reply_to_message.text.split()[4][1:]
    request_text = " ".join(message.reply_to_message.text.split()[7:])
    try:
        await asyncio.create_task(create_user_req(user_id, username, request_text))
    except openai.BadRequestError as e:
        await bot.send_message(message.chat.id, messages.WAIT)
        await bot.send_message(ADMIN_ID, messages.WAIT + e)
    except Exception as e:
        await bot.send_message(ADMIN_ID, messages.UNKNOWN_ERROR + e)


@dp.message_handler(state=UserState.gpt_request)
@dp.message_handler(state=default_state)
async def user_gpt_req_handler(message: types.Message):
    if message.chat.id == ADMIN_ID:
        await bot.send_message(ADMIN_ID, messages.CHECK_PAYMENT.format(message.chat.id, message.chat.username))
        if not check_payment(message.chat.id):
            await bot.send_message(
                message.chat.id,
                messages.EXPIRED_PAYMENT.format(config.PRICE),
                reply_markup=payment_markup(),
            )
            await bot.send_message(ADMIN_ID,
                                   messages.USER_EXPIRED_PAYMENT.format(message.chat.id, message.chat.username))
            return
    request_text = message.text
    try:
        await asyncio.create_task(create_user_req(message.chat.id, message.chat.username, request_text))
    except openai.BadRequestError as e:
        await bot.send_message(message.chat.id, messages.WAIT)
        await bot.send_message(ADMIN_ID, messages.WAIT + e)
    except Exception as e:
        await bot.send_message(ADMIN_ID, messages.UNKNOWN_ERROR + e)
