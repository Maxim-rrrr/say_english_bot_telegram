from loguru import logger

@logger.catch
def registration_user(User, message):
    if not User.find_one({'_id': message.chat.id}):
        try:
            User.insert_one({
                '_id': message.chat.id,
                'name': f'{message.from_user.first_name} {message.from_user.last_name}',
                'username': 'message.from_user.username',
                'classes': []
            })
            logger.info('Успешное добавление пользователя в БД')
            logger.info(
                f'chat_id: {message.chat.id}, Имя: {message.from_user.first_name} {message.from_user.last_name},',
                f' username: {message.from_user.username}')
        except:
            logger.error('Ошибка сохранения пользователя в БД')