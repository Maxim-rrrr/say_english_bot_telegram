from aiogram import types

from controllers.Admin.main import bot_dp
from controllers.Admin.modules.is_auth import is_auth


@bot_dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await is_auth(message)
