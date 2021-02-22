def get(database):
    return database.content.find_one({'_id': 'about_us'})['content']


def set(database, option, content=''):
    database_content = database.content.find_one({'_id': 'about_us'})['content']
    database_content[option] = content

    database.content.update_one({'_id': 'about_us'}, {'$set': {'content': database_content}})

