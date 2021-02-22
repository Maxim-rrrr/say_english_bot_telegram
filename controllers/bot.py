from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import ValidationError
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger

from config import config


try:
    bot = Bot(config['bot_token'])
    bot_dp = Dispatcher(bot, storage=MemoryStorage())
    logger.info('Прошли верификацию bot token.')
except ValidationError:
    logger.error('Ошибка верификации bot token.')
