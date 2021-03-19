from aiogram import types
from aiogram.dispatcher.filters.state import State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,  InlineKeyboardMarkup, \
    ReplyKeyboardRemove, ForceReply, InlineKeyboardButton, CallbackQuery

from loguru import logger
import typing

from DataBase.main import database
from controllers.bot import bot_dp
from controllers.standard_answer import standard_answer
from controllers.Admin.admin_markup import admin_markup
from States import States


def standard_section(
        name: str,
        section_state: State,
        markup: typing.Union[
            InlineKeyboardMarkup,
            ReplyKeyboardMarkup,
            ReplyKeyboardRemove,
            ForceReply,
            None,
        ] = None
    ):

    # Создание стартовой структуры в БД, если её нет
    database.migrate_standard_section(name)

    # Хендлер клиента
    @bot_dp.message_handler(text=name)
    async def get(message: types.Message):
        database.registration_user(message)
        await standard_answer(message, database.get(name), markup)

    # Инлайн клавиатура админа для изменения секции
    options_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('Удалить Текст', callback_data=f'{name}:del_text')],
            [InlineKeyboardButton('Удалить Изображение', callback_data=f'{name}:del_img')],
            [InlineKeyboardButton('Удалить Видео', callback_data=f'{name}:del_video')],
            [InlineKeyboardButton('Удалить Документ', callback_data=f'{name}:del_doc')],
            [InlineKeyboardButton('Изменить', callback_data=f'{name}:edit')]
        ]
    )

    edit_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Завершиить изменения')
    )

    # Хендлер админа
    @bot_dp.message_handler(text=name, state=States.admin)
    async def admin_get(message: types.Message):
        await standard_answer(message, database.get(name))
        await message.answer(f'Опции секции "{name}"', reply_markup=options_keyboard)

    # Хендлер для каллбеков options_keyboard
    @bot_dp.callback_query_handler(text_contains=name, state=States.admin)
    async def callback(call: CallbackQuery):
        data = call.data.split(':')[1]
        print(call.data)
        try:
            if data == 'del_text':
                database.set(name, option='text')
                logger.info(f'Изменение секции\tcallbackData:\t{call.data}')
                await call.message.answer('Успешно!')
            elif data == 'del_img':
                database.set(name, option='photo')
                logger.info(f'Изменение секции\tcallbackData:\t{call.data}')
                await call.message.answer('Успешно!')
            elif data == 'del_video':
                database.set(name, option='video')
                logger.info(f'Изменение секции\tcallbackData:\t{call.data}')
                await call.message.answer('Успешно!')
            elif data == 'del_doc':
                database.set(name, option='document')
                logger.info(f'Изменение секции\tcallbackData:\t{call.data}')
                await call.message.answer('Успешно!')
            elif data == 'edit':
                # Изменяем состояние на изменение именно этой секции
                await section_state.set()
                await call.message.answer(f'Изменение секции "{name}"', reply_markup=edit_keyboard)

        except:
            logger.error(f'Ошибка изменения секции\tcallbackData:\t{call.data}')
            await call.message.answer('Ошибка')

    # Выход из измения
    @bot_dp.message_handler(text='Завершиить изменения', state=section_state)
    async def s(message: types.Message):
        await States.admin.set()
        await message.answer('ОК', reply_markup=admin_markup)

    # Ниже изменения разделённые по типам файлов
    @bot_dp.message_handler(state=section_state, content_types=['text'])
    async def s(message: types.Message):
        logger.info(f'Изменение "{name}" text')
        database.set(name, option='text', content=message.text)
        await message.answer('ОК')

    @bot_dp.message_handler(state=section_state, content_types=['photo'])
    async def s(message: types.Message):
        logger.info(f'Изменение "{name}" photo')
        database.set(name, option='photo', content=message.photo[-1].file_id)
        await message.answer('ОК')

    @bot_dp.message_handler(state=section_state, content_types=['video'])
    async def s(message: types.Message):
        logger.info(f'Изменение "{name}" video')
        database.set(name, option='video', content=message.video.file_id)
        await message.answer('ОК')

    @bot_dp.message_handler(state=section_state, content_types=['document'])
    async def s(message: types.Message):
        logger.info(f'Изменение "{name}" document')
        database.set(name, option='document', content=message.document.file_id)
        await message.answer('ОК')
