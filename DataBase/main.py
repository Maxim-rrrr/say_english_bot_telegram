from pymongo import MongoClient
from loguru import logger

from DataBase.migration import migration
from config import config
from aiogram import types
from datetime import datetime


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

    @logger.catch()
    def get_users(self) -> list:
        User = self.telegram_bot.users
        return list(User.find())

    @logger.catch()
    def add_event(self, content: dict, age_groups: list, reactions: dict) -> int:
        Events = self.telegram_bot.events
        id = len(list(Events.find())) + 1

        self.telegram_bot.events.insert_one({
            '_id': id,
            'content': content,
            'age_groups': age_groups,
            'answers': reactions,
            'user_answer': [],
            'datetime': datetime.today()
        })

        return id

    @logger.catch()
    def answer_event(self, id: int, reaction: str, chat_id: str) -> None:
        event = self.telegram_bot.events.find_one({'_id': id})
        if chat_id not in event['user_answer']:
            user_answer = event['user_answer']
            user_answer.append(chat_id)

            answers = event['answers']
            answers[reaction] += 1
            self.telegram_bot.events.update_one({'_id': id}, {'$set': {
                'answers': answers,
                'user_answer': user_answer
            }})

    @logger.catch()
    def get_event(self, index: int = None):
        events = list(self.telegram_bot.events.find())

        if index is None:
            return events
        return events[index]


database = DB(config['mongo_connect'])
