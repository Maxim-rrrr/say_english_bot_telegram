from pymongo import MongoClient
from configure import config
from loguru import logger
from modules.init_database import init_database


def connect_db():
    global db
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


db = MongoClient(config['mongo_connect']).telegram_bot

