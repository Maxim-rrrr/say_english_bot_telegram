from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from controllers.bot import bot_dp
from States import States
from DataBase.main import database
from controllers.standard_answer import standard_answer

edit_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Последние уведомление')
).add(
    KeyboardButton('Все уведомления')
).add(
    KeyboardButton('Создать уведомление')
).add(
    KeyboardButton('Назад')
)


@bot_dp.message_handler(text='Уведомления', state=States.admin)
async def events(message: types.Message):
    await message.answer('Уведомления', reply_markup=edit_keyboard)


@bot_dp.message_handler(text='Последние уведомление', state=States.admin)
async def events(message: types.Message):
    event = database.get_event(-1)

    await standard_answer(message, event['content'])
    info = f'Дата публикации: {event["datetime"]}\n' + \
           f'Возрастные группы: {event["age_groups"]}\n\n'

    if event['answers']:
        info += f'Реакции:\n' + \
                f' - Всего: {len(event["user_answer"])}\n'

        reactions = event['answers']
        for react in reactions.keys():
            info += f' - "{react}": {reactions[react]}\n'
    else:
        info += 'Реакций нет'

    await message.answer(info)


@bot_dp.message_handler(text='Все уведомления', state=States.admin)
async def events(message: types.Message):
    events = database.get_event()

    li = ''
    for index in range(len(events)):
        event = events[index]
        li += f'{index + 1}. {event["datetime"]}\n'

    await message.answer(li)
    await message.answer('Чтобы узнать информацию по конкретному уведомлению напишите:\n' +
                         '"УВ<Номер>" Например - УВ10')


@bot_dp.message_handler(text_contains='УВ', state=States.admin)
async def events(message: types.Message):
    index = int(message.text[2:]) - 1
    event = database.get_event(index)

    await standard_answer(message, event['content'])
    info = f'Дата публикации: {event["datetime"]}\n' + \
           f'Возрастные группы: {event["age_groups"]}\n\n'

    if event['answers']:
        info += f'Реакции:\n' + \
                f' - Всего: {len(event["user_answer"])}\n'

        reactions = event['answers']
        for react in reactions.keys():
            info += f' - "{react}": {reactions[react]}\n'
    else:
        info += 'Реакций нет'

    await message.answer(info)

import controllers.Admin.create_event