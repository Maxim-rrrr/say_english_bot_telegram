from aiogram import types

from controllers.bot import bot_dp
from DataBase.main import database
from controllers.Admin.modules.standard_answer import standard_answer
from States import State


@bot_dp.message_handler(text='Цены', state=State.admin)
async def prices(message: types.Message):
    await standard_answer(message, database.get_prices())
