from aiogram import Bot, Dispatcher, types
from loguru import logger
from modules.db import db
from configure import config


@logger.catch
def AdminController():
    try:
        bot = Bot(config['bot_admin_token'])
        bot_dp = Dispatcher(bot)
        logger.info('Прошли верификацию admin-bot token.')
    except:
        logger.error('Ошибка верификации admin-bot token.')

    return bot_dp
