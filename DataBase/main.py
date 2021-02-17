from pymongo import MongoClient
from loguru import logger

from DataBase.migration import migration
from configure import config

from DataBase.modules import hello, about_us, admin, faq, user, timetable, teachers, prices


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
        Запись всех пользователей нужна для отправки уведоилений 
        По большому счёту можно хранить только chat ID
    '''
    @logger.catch()
    def registration_user(self, message) -> None:
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

    # Проверка на админа
    @logger.catch()
    def is_admin(self, message):
        return self.telegram_bot.admins.find_one({'_id': message.chat.id})

    # Авторизация админа
    @logger.catch()
    def add_admin(self, message):
        self.telegram_bot.admins.insert_one({
            '_id': message.chat.id,
            'name': f'{message.from_user.first_name} {message.from_user.last_name}',
            'username': f'{message.from_user.username}'
        })

    # Приветствие
    @logger.catch()
    def get_hello(self) -> dict:
        return hello.get(self.telegram_bot)

    @logger.catch()
    def set_hello(self, content) -> str:
        return hello.set(self.telegram_bot, content)

    # О нас
    @logger.catch()
    def get_about(self) -> dict:
        return about_us.get(self.telegram_bot)

    @logger.catch()
    def set_about(self, content) -> str:
        pass

    # Преподаватели
    @logger.catch()
    def get_teachers(self) -> dict:
        return teachers.get(self.telegram_bot)

    @logger.catch()
    def set_teachers(self, content) -> str:
        pass

    # Цены
    @logger.catch()
    def get_prices(self) -> dict:
        return prices.get(self.telegram_bot)

    @logger.catch()
    def set_prices(self, content) -> str:
        pass

    # Расписание
    @logger.catch()
    def get_timetable(self) -> dict:
        return timetable.get(self.telegram_bot)

    @logger.catch()
    def set_timetable(self, content) -> str:
        pass

    # Измениение возраста ребёнка
    @logger.catch()
    def edit_age_group(self, chat_id: str, value: str) -> None:
        self.telegram_bot.users.update_one({'_id': chat_id}, {'$set': {
            'age_group': value
        }})


database = DB(config['mongo_connect'])
