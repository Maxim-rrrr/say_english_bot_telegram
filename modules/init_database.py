"""
    Здесь у нас инициализация стартовых записей в БД
"""


def init_database(db):
    User = db.users
    Content = db.content

    if not Content.find_one({'_id': 'start_info'}):
        Content.insert_one({'_id': 'start_info', 'text': 'Языковой центр SAY'})
