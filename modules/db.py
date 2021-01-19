from pymongo import MongoClient
from configure import config
from loguru import logger
from modules.init_database import init_database


def check_db():
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


@logger.catch
def get_info():
    Content = db.content
    return Content.find_one({'_id': 'start_info'})['text']


@logger.catch
def registration_user(message):
    User = db.users
    if not User.find_one({'_id': message.chat.id}):
        try:
            User.insert_one({
                '_id': message.chat.id,
                'name': f'{message.from_user.first_name} {message.from_user.last_name}',
                'username': f'{message.from_user.username}',
                'classes': []
            })
            logger.info('Успешное добавление пользователя в БД')
            logger.info(
                f'chat_id: {message.chat.id}, Имя: {message.from_user.first_name} {message.from_user.last_name}, username: {message.from_user.username}'
            )
        except:
            logger.error('Ошибка сохранения пользователя в БД')


@logger.catch()
def set_info(text):
    Content = db.content
    Content.update_one({'_id': 'start_info'}, {'$set': {'text': text}})


@logger.catch()
def add_admin(message):
    Admin = db.admins
    Admin.insert_one({
        '_id': message.chat.id,
        'name': f'{message.from_user.first_name} {message.from_user.last_name}',
        'username': f'{message.from_user.username}'
    })


@logger.catch()
def is_admin(message):
    Admin = db.admins
    return Admin.find_one({'_id': message.chat.id})


db = MongoClient(config['mongo_connect']).telegram_bot


