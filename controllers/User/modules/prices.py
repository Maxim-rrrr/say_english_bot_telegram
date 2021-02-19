from aiogram import types

from controllers.User.main import bot_dp
from DataBase.main import database
from controllers.User.modules.standard_answer import standard_answer


@bot_dp.message_handler(text='Цены')
async def prices(message: types.Message):
    await standard_answer(message, database.get_prices())