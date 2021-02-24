from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,  InlineKeyboardMarkup, \
    ReplyKeyboardRemove, ForceReply, InlineKeyboardButton, CallbackQuery

from loguru import logger
from pprint import pprint

from controllers.bot import bot_dp
from States import States
from DataBase.main import database
from controllers.Admin.admin_markup import admin_markup


edit_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отмена')
).add(
    KeyboardButton('Предпросмотр')
).add(
    KeyboardButton('Выбрать возраст')
).add(
    KeyboardButton('Опубликовать')
)


@bot_dp.message_handler(text='Создания уведомления', state=States.admin)
async def create_event(message: types.Message):
    States.create_event.set()
    await message.answer('Создание уведомления', reply_markup=edit_keyboard)


# Хендел отмены
@bot_dp.message_handler(text='Отмена', state=States.create_event)
async def s(message: types.Message):
    await States.admin.set()
    await message.answer('ОК', reply_markup=admin_markup)


# Хендел Предпросмотр
@bot_dp.message_handler(text='Предпросмотр', state=States.create_event)
async def s(message: types.Message):
    pass


# Хендел Выбора возраста
@bot_dp.message_handler(text='Выбрать возраст', state=States.create_event)
async def s(message: types.Message):
    pass


# Хендел публикации
@bot_dp.message_handler(text='Опубликовать', state=States.create_event)
async def s(message: types.Message):
    pass


# Приём всех файлов по типам
@bot_dp.message_handler(state=States.create_event, content_types=['text'])
async def s(message: types.Message):
    # logger.info(f'Изменение "{name}" text')
    # database.set(name, option='text', content=message.text)
    await message.answer('ОК')


@bot_dp.message_handler(state=States.create_event, content_types=['photo'])
async def s(message: types.Message):
    # logger.info(f'Изменение "{name}" photo')
    # database.set(name, option='photo', content=message.photo[-1].file_id)
    await message.answer('ОК')


@bot_dp.message_handler(state=States.create_event, content_types=['video'])
async def s(message: types.Message):
    # logger.info(f'Изменение "{name}" video')
    # database.set(name, option='video', content=message.video.file_id)
    await message.answer('ОК')


@bot_dp.message_handler(state=States.create_event, content_types=['document'])
async def s(message: types.Message):
    # logger.info(f'Изменение "{name}" document')
    # database.set(name, option='document', content=message.document.file_id)
    await message.answer('ОК')
