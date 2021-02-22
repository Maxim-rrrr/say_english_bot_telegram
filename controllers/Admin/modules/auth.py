from aiogram import types

from configure import config
from DataBase.main import database
from controllers.Admin.modules.is_auth import is_auth
from controllers.Admin.main import bot_dp
from controllers.Admin.modules.admin_markup import core_markup


@bot_dp.message_handler(text=[config['admin_password']])
async def auth(message: types.Message):
    if await is_auth(message):
        return

    database.add_admin(message)
    await message.answer('Авторизация успешна', reply_markup=core_markup)