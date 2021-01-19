from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger
from modules.db import get_info, set_info, is_admin, add_admin
from configure import config


@logger.catch
def AdminController():
    try:
        admin = Bot(config['bot_admin_token'])
        admin_dp = Dispatcher(admin)
        logger.info('Прошли верификацию admin-bot token.')
    except:
        logger.error('Ошибка верификации admin-bot token.')

    core_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Основная информация')
    ).add(
        KeyboardButton('FAQ')
    )


    @admin_dp.message_handler(commands=['start'])
    async def start_admin(message: types.Message):
        await admin.send_message(message.from_user.id, 'Введите пароль авторизации', reply_markup=core_markup)

    @admin_dp.message_handler()
    async def info(message: types.Message):
        if is_admin(message):
            if message.text == 'Основная информация':
                await message.answer(get_info() + '\n\nОтправьте сообщение начинающееся с "edit_info" и оно станет новой "Основной информацией"')

            if message.text.startswith('edit_info'):
                if message.text[9:].strip():
                    set_info(message.text[9:].strip())
                    await message.answer('OK') 

        elif message.text == config['admin_password']:
            add_admin(message)
            await message.answer('Авторизация успешна')
        else:
            await message.answer('Введите пароль авторизации')

    return admin, admin_dp
