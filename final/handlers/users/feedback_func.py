import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from config import ADMIN_ID
from constants.messages import *
from database.feedback_db import add_new_feedback
from database.feedback_db import delete_user_from_feedback, get_all_feed_back_users
from keyboards.keyboards import feedback_markup
from .start_command import UserState
from loader import bot, dp


@dp.callback_query_handler(text='give_feedback', state="*")
async def get_feedback_handler(call: types.CallbackQuery):
    await call.message.edit_text(FEEDBACK_PROMPT)
    await UserState.feedback.set()


@dp.message_handler(state=UserState.feedback)
async def feedback_handler(message: types.Message, state: FSMContext):
    await state.finish()
    add_new_feedback(message.chat.id, message.text)
    await bot.send_message(
        ADMIN_ID,
        NEW_FEEDBACK.format(message.chat.id, message.chat.username, message.text),
    )


async def start_feed_back():
    all_users = get_all_feed_back_users()
    for user in all_users:
        try:
            await bot.send_message(
                user[0],
                text=FEEDBACK,
                reply_markup=feedback_markup(),
            )
            delete_user_from_feedback(user[0])
            await asyncio.sleep(0.2)
        except:
            continue
    await asyncio.sleep(8640)
