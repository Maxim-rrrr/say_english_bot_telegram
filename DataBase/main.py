from pymongo import MongoClient
from loguru import logger

from DataBase.migration import migration
from config import config
from aiogram import types


class DB(MongoClient):
    @logger.catch()
    def __init__(self, host=None):
        try:
            super().__init__(host, port=None, document_class=dict, tz_aware=None, connect=None, type_registry=None)
            logger.info('База данных подключена.')
        except:
            logger.error('Ошибка подключения БД.')

        migration(self.telegram_bot)
        logger.info('Проверка целостности БД завершина.')

    '''
        Запись всех пользователей нужна для отправки уведомлений 
        По большому счёту можно хранить только chat ID
    '''
    @logger.catch()
    def registration_user(self, message: types.Message) -> None:
        User = self.telegram_bot.users
        if not User.find_one({'_id': message.chat.id}):
            try:
                User.insert_one({
                    '_id': message.chat.id,
                    'name': f'{message.from_user.first_name} {message.from_user.last_name}',
                    'username': f'{message.from_user.username}',
                    'age_group': ''
                })
                logger.info('Успешное добавление пользователя в БД')
                logger.info(
                    f'chat_id: {message.chat.id}, Имя: {message.from_user.first_name} {message.from_user.last_name}, username: {message.from_user.username}'
                )
            except:
                logger.error('Ошибка сохранения пользователя в БД')

    def get(self, name: str) -> dict:
        return self.telegram_bot.content.find_one({'_id': name})['content']

    def set(self, name: str, option: str, content: str = '') -> None:
        database_content = self.telegram_bot.content.find_one({'_id': name})['content']
        database_content[option] = content

        self.telegram_bot.content.update_one({'_id': name}, {'$set': {'content': database_content}})

    # Измениение возраста ребёнка
    @logger.catch()
    def edit_age_group(self, chat_id: str, value: str) -> None:
        self.telegram_bot.users.update_one({'_id': chat_id}, {'$set': {
            'age_group': value
        }})

    # Миграция стандартной секции
    @logger.catch()
    def migrate_standard_section(self, name: str) -> None:
        Content = database.telegram_bot.content

        if not Content.find_one({'_id': name}):
            Content.insert_one({
                '_id': name,
                'content': {
                    'text': name,
                    'photo': '',
                    'video': '',
                    'document': ''
                }
            })


database = DB(config['mongo_connect'])
