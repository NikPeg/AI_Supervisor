from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

FEEDBACK = InlineKeyboardButton(text="👌Оставить отзыв", callback_data='give_feedback')

BACK = InlineKeyboardButton(text='👈Назад', callback_data='return')

ABOUT = InlineKeyboardButton(text="ℹ️Узнать о frAId", callback_data='info'),
SOS = InlineKeyboardButton(text='🆘Поддержка', url=config.SOS_URL),
