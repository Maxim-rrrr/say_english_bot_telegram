def get(database):
    return database.content.find_one({'_id': 'hello'})['content']


def set(database, content):
    database.content.update_one({'_id': 'hello'}, {'$set': {'content': content}})

