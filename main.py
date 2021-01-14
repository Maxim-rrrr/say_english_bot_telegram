from pymongo import MongoClient
import telebot
from loguru import logger

from configure import config
from view.start_info import start_info
from modules.init_database import init_database
from modules.registration_user import registration_user

# Настойки логера
logger.add('logs/logs.log', format='{time} {level} {message}', level='DEBUG', rotation='1 MB', compression='zip')

# Инициализация MongoDB
mongo_client = MongoClient(config['mongo_connect'])
logger.info('База данных подключена.')
db = mongo_client.telegram_bot

# Определение коллекций БД
User = db.users
Content = db.content

# Инициализация стартовых записей в БД
init_database(db)
logger.info('Проверка целостности БД завершина.')

# Инициализация Telegam bot
bot = telebot.TeleBot(config['bot_token'])
logger.info('Прошли верификацию bot token.')


# функция отвечающая на текстовые сообщения
@bot.message_handler(content_types=['text'])
def response_text(message):
    # Всех пользователей заносим в БД
    registration_user(User, message)

    if message.text == '/start':
        start_info(db, bot, message.chat.id)


bot.polling(none_stop=True)
