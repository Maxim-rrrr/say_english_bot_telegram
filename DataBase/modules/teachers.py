def get(database):
    return database.content.find_one({'_id': 'teachers'})['content']
