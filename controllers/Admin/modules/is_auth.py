from aiogram import types

from configure import config
from DataBase.main import database


# Проверка на авторизацию
async def is_auth(message: types.Message):
    if not database.is_admin(message):
        if message.text != config['admin_password']:
            await message.answer('Введите пароль авторизации')
        return False
    return True
