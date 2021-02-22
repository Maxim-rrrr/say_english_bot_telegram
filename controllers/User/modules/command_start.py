from aiogram import types

from controllers.bot import bot_dp
from DataBase.main import database
from controllers.User.modules.core_markup import core_markup
from controllers.User.modules.standard_answer import standard_answer

@bot_dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Всех пользователей заносим в БД
    database.registration_user(message)
    await standard_answer(message, database.get_hello(), core_markup)