import asyncio

from loader import dp,bot
from aiogram import types
from keyboards.keyboards import start_markup,return_markup
from messages import fr_mess,start_mess,start_mess_2,help_mess,help_mess_2,new_mess
from aiogram.dispatcher.filters.state import State,StatesGroup
from database.sessia_db import create_new_sessia
from database.mess_db import add_new_message
from database.users_db import add_new_user
from config import admin_id




class User_(StatesGroup):
    gpt_req = State()
    feedback = State()

@dp.message_handler(commands=['start'],state="*")
async def start_command_handler(message:types.Message):
    add_new_user(message.chat.id, message.chat.username)
    await bot.send_message(message.chat.id, start_mess,reply_markup=start_markup())
    create_new_sessia(message.chat.id)
    await bot.send_message(message.chat.id,start_mess_2)
    await bot.send_message(admin_id, f"Пользователь {message.chat.id} c ником {message.chat.username} нажал кнопку /start.")
    await User_.gpt_req.set()

@dp.callback_query_handler(text='info',state="*")
async def info_handler(call:types.CallbackQuery):
    await call.message.edit_text(fr_mess,reply_markup=return_markup())
    await bot.send_message(admin_id, f"Пользователь {call.message.chat.id} c ником {call.message.chat.username} нажал кнопку ℹ️Узнать о frAId.")


@dp.callback_query_handler(text='return',state="*")
async def return_handler(call:types.CallbackQuery):
    await call.message.edit_text(start_mess,reply_markup=start_markup())
    await bot.send_message(admin_id, f"Пользователь {call.message.chat.id} c ником {call.message.chat.username} нажал кнопку Назад.")



@dp.message_handler(commands=['help'],state="*")
async def help_message_handler(message:types.Message):
    await bot.send_message(message.chat.id, fr_mess)
    await bot.send_message(message.chat.id, start_mess_2)
    await bot.send_message(admin_id, f"Пользователь {message.chat.id} c ником {message.chat.username} нажал кнопку /help.")


@dp.message_handler(commands=['new'],state="*")
async def help_message_handler(message:types.Message):
    await bot.send_message(message.chat.id, new_mess)
    create_new_sessia(message.chat.id)
    await bot.send_message(admin_id, f"Пользователь {message.chat.id} c ником {message.chat.username} нажал кнопку /new.")
    await User_.gpt_req.set()

@dp.message_handler(state=User_.gpt_req)
async def user_gpt_req_handler(message:types.Message):
    req_text = message.text
    await asyncio.create_task(create_user_req(message.chat.id, message.chat.username, req_text))

async def create_user_req(user_id,user_name,req_text):
    from gpt_func import gpt_ask_func
    bot_req = gpt_ask_func(req_text)
    add_new_message(user_id, req_text, bot_req)
    await bot.send_message(user_id, bot_req)
    await bot.send_message(admin_id,
                           f"Пользователь {user_id} c ником @{user_name} прислал сообщение {req_text}.\n\n"
                           f"ChatGPT ответил: {bot_req}."
                           )


