from aiogram import types

from controllers.Admin.main import bot_dp
from DataBase.main import database
from controllers.Admin.modules.is_auth import is_auth
from controllers.Admin.modules.standard_answer import standard_answer


@bot_dp.message_handler(text='Часто задаваемые вопросы')
async def faq(message: types.Message):
    if not await is_auth(message):
        return

    await message.answer('FAQ')
