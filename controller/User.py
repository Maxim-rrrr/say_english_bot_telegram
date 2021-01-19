from aiogram import Bot, Dispatcher, types
from loguru import logger
from modules.db import registration_user, get_info
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

        # Всех пользователей заносим в БД
        registration_user(message)
        if message.text == '/start':
            await message.answer(get_info())

    return bot, bot_dp
