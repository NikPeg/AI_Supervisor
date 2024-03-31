from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def feedback_markup():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.insert(InlineKeyboardButton(text='Оставить отзыв', callback_data='give_feedback'))
    return markup


def start_markup():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text='ℹ️Узнать о frAId', callback_data='info'),
        InlineKeyboardButton(text='🆘Поддержка', url='http://t.me/nikpeg'),
    )
    return markup


def return_markup():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(InlineKeyboardButton(text='Назад', callback_data='return'))
    return markup
