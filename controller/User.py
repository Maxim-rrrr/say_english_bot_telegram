from aiogram import Bot, Dispatcher, types
from view.start_info import start_info
from modules.registration_user import registration_user
from loguru import logger
from modules.db import db
from configure import config


@logger.catch
def UserController():
    try:
        bot = Bot(config['bot_token'])
        bot_dp = Dispatcher(bot)
        logger.info('Прошли верификацию bot token.')
    except:
        logger.error('Ошибка верификации bot token.')

    # функция отвечающая на текстовые сообщения
    @bot_dp.message_handler()
    async def response_text(message: types.Message):
        User = db.users
        # Всех пользователей заносим в БД
        registration_user(User, message)
        if message.text == '/start':
            await start_info(db, message)

    return bot_dp
