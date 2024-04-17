from aiogram import types
from aiogram.dispatcher import FSMContext
from config import ADMIN_ID

import messages
from database.feedback_db import add_new_feedback
from database.feedback_db import delete_user_from_feedback
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
