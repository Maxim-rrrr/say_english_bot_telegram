from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher import FSMContext

from loguru import logger
from pprint import pprint

from controllers.bot import bot, bot_dp
from States import States
from DataBase.main import database
from controllers.Admin.admin_markup import admin_markup
from controllers.standard_answer import standard_answer

edit_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отмена')
).add(
    KeyboardButton('Предпросмотр')
).add(
    KeyboardButton('Выбрать возраст')
).add(
    KeyboardButton('Добавить реакцию')
).add(
    KeyboardButton('Опубликовать')
)


@bot_dp.message_handler(text='Создать уведомление', state=States.admin)
async def create_event(message: types.Message):
    await States.create_event.set()
    await message.answer('Создание уведомления', reply_markup=edit_keyboard)


# Хендел отмены
@bot_dp.message_handler(text='Отмена', state=States.create_event)
async def s(message: types.Message, state: FSMContext):
    await state.reset_state()
    await States.admin.set()
    await message.answer('ОК', reply_markup=admin_markup)


# Хендел Предпросмотр
@bot_dp.message_handler(text='Предпросмотр', state=States.create_event)
@logger.catch()
async def s(message: types.Message, state: FSMContext):
    data = await state.get_data()
    pprint(data)
    await standard_answer(message, {
        'text': data.get('text_event'),
        'photo': data.get('photo_event'),
        'video': data.get('video_event'),
        'document': data.get('document_event'),
    })

    if data.get('reaction'):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(reaction, callback_data='viewing_reaction')] for reaction in data.get('reaction')
            ]
        )

        await message.answer('Оставьте реакцию', reply_markup=markup)


# Хендел Выбора возраста
@bot_dp.message_handler(text='Выбрать возраст', state=States.create_event)
async def s(message: types.Message, state: FSMContext):
    choice_age_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('6-8 лет', callback_data='age:6-8')],
            [InlineKeyboardButton('9-11 лет', callback_data='age:9-11')],
            [InlineKeyboardButton('12-14 лет', callback_data='age:12-14')],
            [InlineKeyboardButton('15-18 лет', callback_data='age:15-18')],
            [InlineKeyboardButton('18+ лет', callback_data='age:18+')]
        ]
    )

    await message.answer(
        'Выберете возрастные группы, которым отправлять это уведомление. (Если не выбрать ничего то придёт всем)',
        reply_markup=choice_age_keyboard
    )


@bot_dp.callback_query_handler(text_contains='age', state=States.create_event)
async def callback_choice_age(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('age_groups'):
        if call.data.split(':')[1] not in data['age_groups']:
            data['age_groups'].append(call.data.split(':')[1])
            await state.update_data(age_groups=data['age_groups'])
    else:
        await state.update_data(age_groups=[call.data.split(':')[1]])

    data = await state.get_data()
    await call.message.answer(data.get('age_groups'))


# Хендел добавление реакции
@bot_dp.message_handler(text='Добавить реакцию', state=States.create_event)
async def s(message: types.Message, state: FSMContext):
    await States.add_event_reaction.set()

    edit_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отмена')
    )

    await message.answer(
        f'Напишите сообщение в формате:\nКнопка1 / Кнопка2 / Кнопка3\n\nРазделение через " / "\nНе забывайте пробелы',
        reply_markup=edit_keyboard)


@bot_dp.message_handler(text='Отмена', state=States.add_event_reaction)
async def s(message: types.Message, state: FSMContext):
    await States.create_event.set()
    await message.answer('ОК', reply_markup=edit_keyboard)


@bot_dp.message_handler(content_types=['text'], state=States.add_event_reaction)
async def s(message: types.Message, state: FSMContext):
    content = message.text.split(' / ')
    if content:
        await States.create_event.set()
        await state.update_data(reaction=content)
        await message.answer('ОК', reply_markup=edit_keyboard)
    else:
        await message.answer(
            f'Напишите сообщение в формате:\nКнопка1 / Кнопка2 / Кнопка3\n\nРазделение через " / "\nНе забывайте пробелы')


@bot_dp.callback_query_handler(text_contains='reaction')
async def callback(call: CallbackQuery):
    data = call.data.split(':')
    id = data[1]
    reaction = data[2]

    database.answer_event(int(id), reaction, call.message.chat.id)


# Хендел публикации
@bot_dp.message_handler(text='Опубликовать', state=States.create_event)
async def s(message: types.Message, state: FSMContext):
    data = await state.get_data()
    content = {
        'text': data.get('text_event'),
        'photo': data.get('photo_event'),
        'video': data.get('video_event'),
        'document': data.get('document_event')
    }

    count_users = 0

    if not data.get('age_groups'):
        for user in database.get_users():
            if content['text']:
                await bot.send_message(user['_id'], content['text'])
            if content['photo']:
                await bot.send_photo(user['_id'], content['photo'])
            if content['video']:
                await bot.send_video(user['_id'], content['video'])
            if content['document']:
                await bot.send_document(user['_id'], content['document'])

            count_users += 1
    else:
        for user in database.get_users():
            if not user['age_group'] or user['age_group'] in data.get('age_groups'):
                if content['text']:
                    await bot.send_message(user['_id'], content['text'])
                if content['photo']:
                    await bot.send_photo(user['_id'], content['photo'])
                if content['video']:
                    await bot.send_video(user['_id'], content['video'])
                if content['document']:
                    await bot.send_document(user['_id'], content['document'])

                count_users += 1
    '''
        Здесь мы собираем в кучу все данные о уведомлении:
        content: {
            text: ''
            photo: ''
            video: ''
            document: ''
        },
        age_groups: [],
        reactions: {
            реакция: кол-во ответов, 
            ...
        }
        
        и отправляем в БД методом add_event
        обратно получаем id уведомления и уже с id отправляем саму клаву с реакциями
    '''
    reactions = {}
    for react in data.get('reaction', []):
        reactions[react] = 0

    id = database.add_event(content, data.get('age_groups', []), reactions)

    if reactions:

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(reaction, callback_data=f'reaction:{id}:{reaction}')] for reaction in reactions
            ]
        )

        await message.answer('Оставьте ответ)', reply_markup=markup)

    await state.reset_state()
    await States.admin.set()

    logger.info(
        f'Уведомление отправлено {count_users} пользователям\n{content}\nВозрастные группы: {data.get("age_groups")}\nРеакции: {reactions}')

    await message.answer(f'Уведомление отправлено {count_users} пользователям', reply_markup=admin_markup)


# Приём всех файлов по типам
@bot_dp.message_handler(state=States.create_event, content_types=['text'])
async def s(message: types.Message, state: FSMContext):
    await state.update_data(text_event=message.text)
    await message.answer('ОК')


@bot_dp.message_handler(state=States.create_event, content_types=['photo'])
async def s(message: types.Message, state: FSMContext):
    await state.update_data(photo_event=message.photo[-1].file_id)
    await message.answer('ОК')


@bot_dp.message_handler(state=States.create_event, content_types=['video'])
async def s(message: types.Message, state: FSMContext):
    await state.update_data(video_event=message.video.file_id)
    await message.answer('ОК')


@bot_dp.message_handler(state=States.create_event, content_types=['document'])
async def s(message: types.Message, state: FSMContext):
    await state.update_data(document_event=message.document.file_id)
    await message.answer('ОК')
