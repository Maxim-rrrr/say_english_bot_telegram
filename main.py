from pymongo import MongoClient
from aiogram import Bot, Dispatcher, executor, types
from loguru import logger

from configure import config
from view.start_info import start_info
from modules.init_database import init_database
from modules.registration_user import registration_user

# Настойки логера
logger.add('logs/logs.log', format='{time} {level} {message}', level='DEBUG', rotation='1 MB', compression='zip')

# Инициализация MongoDB
try:
    mongo_client = MongoClient(config['mongo_connect'])
    logger.info('База данных подключена.')
    db = mongo_client.telegram_bot
except:
    logger.error('Ошибка подключения БД.')

# Инициализация стартовых записей в БД
init_database(db)
logger.info('Проверка целостности БД завершина.')

# Определение коллекций БД
User = db.users
Content = db.content

# Инициализация Telegram bot
try:
    bot = Dispatcher(Bot(config['bot_token']))
    logger.info('Прошли верификацию bot token.')
except:
    logger.error('Ошибка верификации bot token.')

# Инициализация Telegram admin-bot
try:
    admin = Dispatcher(Bot(config['bot_admin_token']))
    logger.info('Прошли верификацию admin-bot token.')
except:
    logger.error('Ошибка верификации admin-bot token.')


# функция отвечающая на текстовые сообщения
@bot.message_handler()
async def response_text(message: types.Message):
    # Всех пользователей заносим в БД
    registration_user(User, message)
    print(message)
    if message.text == '/start':
        await start_info(db, message)

if __name__ == '__main__':
    executor.start_polling(bot, skip_updates=True)
    executor.start_polling(admin, skip_updates=True)
