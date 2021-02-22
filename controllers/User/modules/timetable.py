from aiogram import types

from controllers.bot import bot_dp
from DataBase.main import database
from controllers.User.modules.standard_answer import standard_answer


@bot_dp.message_handler(text='Расписание')
async def timetable(message: types.Message):
    await standard_answer(message, database.get_timetable())
