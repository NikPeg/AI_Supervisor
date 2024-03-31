from constants import buttons
from aiogram.types import InlineKeyboardMarkup


def feedback_markup():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.insert(buttons.FEEDBACK)
    return markup


def start_markup():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(buttons.ABOUT, buttons.SOS)
    return markup


def return_markup():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(buttons.BACK)
    return markup
