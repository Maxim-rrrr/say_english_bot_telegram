from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from controllers.bot import bot_dp
from States import States
from DataBase.main import database
from controllers.standard_answer import standard_answer

from controllers.User.childs_age import groups


@bot_dp.message_handler(text='Статистика', state=States.admin)
async def events(message: types.Message):
    users = database.get_users()
    info = f'Всего пользователей: {len(users)}\n'

    count_user = {}
    for group in groups:
        count_user[group] = 0
    count_user['Не выбрали возраст'] = 0

    for user in users:
        if user['age_group']:
            count_user[user['age_group']] += 1
        else:
            count_user['Не выбрали возраст'] += 1

    for group in count_user:
        info += f' - "{group}": {count_user[group]}\n'

    await message.answer(info)