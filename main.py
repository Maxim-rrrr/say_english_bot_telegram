from aiogram import executor, types
from loguru import logger

from config import config
from States import State
from controllers.bot import bot_dp
from controllers.Admin.modules.admin_markup import admin_markup

# Настойки логера
logger.add('logs/user/logs.log', format='{time} {level} {message}', level='DEBUG', rotation='1 MB', compression='zip')


import controllers.User.main


# Авторизацию прокидываем прям тут, а дальше всё через state
@bot_dp.message_handler(text=[config['admin_password']])
async def auth(message: types.Message):
    await State.admin.set()
    await message.answer('Авторизация успешна', reply_markup=admin_markup)


import controllers.Admin.main


if __name__ == '__main__':
    executor.start_polling(bot_dp, skip_updates=True)
