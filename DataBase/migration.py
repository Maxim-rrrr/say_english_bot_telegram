"""
    Здесь инициализация стартовых записей в БД
    Что-то типо миграций
"""
from loguru import logger


@logger.catch
def migration(db):
    Content = db.content

    if not Content.find_one({'_id': 'faq'}):
        Content.insert_one({
            '_id': 'faq',
            'content': [
                {
                    'question': 'Вопрос 1',
                    'answer': 'Ответ 1'
                },
                {
                    'question': 'Вопрос 2',
                    'answer': 'Ответ 2'
                }
            ]
        })


