

def registration_user(User, message):
    if not User.find_one({'_id': message.chat.id}):
        try:
            User.insert_one({
                '_id': message.chat.id,
                'name': f'{message.from_user.first_name} {message.from_user.last_name}',
                'username': 'message.from_user.username',
                'classes': []
            })
            print('Успешное добавление пользователя в БД')
            print(
                f'chat_id: {message.chat.id}, Имя: {message.from_user.first_name} {message.from_user.last_name},',
                f' username: {message.from_user.username}\n')
        except:
            print('Ошибка сохранения пользователя в БД\n')