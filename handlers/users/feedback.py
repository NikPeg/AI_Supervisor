import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

import messages
from config import ADMIN_ID
from database.feedback_db import add_new_feedback
from database.feedback_db import delete_user_from_feedback, get_all_feed_back_users
from keyboards.keyboards import feedback_markup
from loader import bot, dp
from .commands import UserState


@dp.callback_query_handler(text='give_feedback', state="*")
async def get_feedback_handler(call: types.CallbackQuery):
    await call.message.edit_text(messages.FEEDBACK_PROMPT)
    await UserState.feedback.set()


@dp.message_handler(state=UserState.feedback)
async def feedback_handler(message: types.Message, state: FSMContext):
    await state.finish()
    add_new_feedback(message.chat.id, message.text)
    await bot.send_message(
        ADMIN_ID,
        messages.FEEDBACK_SENT.format(message.chat.id, message.chat.username, message.text),
    )
    await bot.send_message(message.chat.id, messages.FEEDBACK_THANK)
    delete_user_from_feedback(message.chat.id)


FEEDBACK_PERIOD = 60 * 60


async def start_feed_back():
    while True:
        all_users = get_all_feed_back_users()
        for user in all_users:
            try:
                await bot.send_message(user[0], text=messages.FEEDBACK_ASK, reply_markup=feedback_markup())
                await bot.send_message(ADMIN_ID, text=messages.FEEDBACK_ASKED.format(user[0]))
                delete_user_from_feedback(user[0])
            except Exception as e:
                await bot.send_message(ADMIN_ID, text=e)
                continue
        await asyncio.sleep(FEEDBACK_PERIOD)