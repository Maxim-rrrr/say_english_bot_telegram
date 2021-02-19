from aiogram import types

from controllers.Admin.main import bot_dp
from DataBase.main import database
from controllers.Admin.modules.is_auth import is_auth
from controllers.Admin.modules.standard_answer import standard_answer


@bot_dp.message_handler(text='Преподаватели')
async def teachers(message: types.Message):
    if not await is_auth(message):
        return

    await standard_answer(message, database.get_teachers())