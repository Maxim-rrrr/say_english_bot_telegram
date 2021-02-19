from aiogram import executor
from loguru import logger

from controllers.Admin.main import bot_dp

# Настойки логера
logger.add('logs/user/logs.log', format='{time} {level} {message}', level='DEBUG', rotation='1 MB', compression='zip')

if __name__ == '__main__':
    executor.start_polling(bot_dp, skip_updates=True)
