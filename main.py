from aiogram import executor
from loguru import logger

from controllers.bot import bot_dp


# Настойки логера
logger.add('logs/logs.log', format='{time} {level} {message}', level='DEBUG', rotation='1 MB', compression='zip')

import controllers.main

if __name__ == '__main__':
    executor.start_polling(bot_dp, skip_updates=True)
