"""
    Здесь инициализация стартовых записей в БД
    Что-то типо миграций
"""
from loguru import logger


@logger.catch
def migration(db):
    Content = db.content

    if not Content.find_one({'_id': 'hello'}):
        Content.insert_one({
            '_id': 'hello',
            'content': {
                'text': 'Приветствие',
                'photo': '',
                'video': '',
                'document': ''
            }
        })

    if not Content.find_one({'_id': 'about_us'}):
        Content.insert_one({
            '_id': 'about_us',
            'content': {
                'text': 'О нас',
                'photo': '',
                'video': '',
                'document': ''
            }
        })

    if not Content.find_one({'_id': 'teachers'}):
        Content.insert_one({
            '_id': 'teachers',
            'content': {
                'text': 'Преподаватели',
                'photo': '',
                'video': '',
                'document': ''
            }
        })

    if not Content.find_one({'_id': 'prices'}):
        Content.insert_one({
            '_id': 'prices',
            'content': {
                'text': 'Цены',
                'photo': '',
                'video': '',
                'document': ''
            }
        })

    if not Content.find_one({'_id': 'timetable'}):
        Content.insert_one({
            '_id': 'timetable',
            'content': {
                'text': 'Расписание',
                'photo': '',
                'video': '',
                'document': ''
            }
        })

    if not Content.find_one({'_id': 'faq'}):
        Content.insert_one({
            '_id': 'faq',
            'content': [
                {
                    'question': 'Вопрос 1',
                    'answer': {
                        'text': 'Ответ 1',
                        'photo': '',
                        'video': '',
                        'document': ''
                    }
                },
                {
                    'question': 'Вопрос 2',
                    'answer': {
                        'text': 'Ответ 2',
                        'photo': '',
                        'video': '',
                        'document': ''
                    }
                }
            ]
        })


