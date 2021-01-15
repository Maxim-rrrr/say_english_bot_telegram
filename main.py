from aiogram import executor
from loguru import logger

from controller.User import UserController
from controller.Admin import AdminController
from modules.db import check_db

# Настойки логера
logger.add('logs/logs.log', format='{time} {level} {message}', level='DEBUG', rotation='1 MB', compression='zip')

# Проверка MongoDB
check_db()

# Регистрация контроллеров
bot_dp = UserController()
admin_dp = AdminController()

if __name__ == '__main__':
    executor.start_polling(bot_dp, skip_updates=True)
    executor.start_polling(admin_dp, skip_updates=True)
