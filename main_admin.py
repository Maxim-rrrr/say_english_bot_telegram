from aiogram import executor
from loguru import logger

from controllers.Admin.main import admin_controller
from DataBase.main import database

# Настойки логера
logger.add('logs/user/logs.log', format='{time} {level} {message}', level='DEBUG', rotation='1 MB', compression='zip')


# Регистрация контроллеров
bot, bot_dp = admin_controller(database)

if __name__ == '__main__':
    executor.start_polling(bot_dp, skip_updates=True)
