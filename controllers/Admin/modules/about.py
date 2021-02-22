from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher import FSMContext
from loguru import logger
from pprint import pprint

from controllers.Admin.main import bot_dp
from DataBase.main import database
from controllers.Admin.modules.is_auth import is_auth
from controllers.Admin.modules.standard_answer import standard_answer

from controllers.Admin.modules.states import EditState
from controllers.Admin.modules.core_markup import core_markup

options_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Удалить Текст', callback_data='about:del_text')],
        [InlineKeyboardButton('Удалить Изображение', callback_data='about:del_img')],
        [InlineKeyboardButton('Удалить Видео', callback_data='about:del_video')],
        [InlineKeyboardButton('Удалить Документ', callback_data='about:del_doc')],
        [InlineKeyboardButton('Изменить', callback_data='about:edit')]
    ]
)

edit_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Завершиить изменения')
)


@bot_dp.message_handler(text='О нас')
async def about(message: types.Message):
    if not await is_auth(message):
        return

    await standard_answer(message, database.get_about())
    await message.answer('Опции секции "О нас"', reply_markup=options_keyboard)


@bot_dp.callback_query_handler(text_contains='about')
async def callback(call: CallbackQuery):
    data = call.data.split(':')[1]
    try:
        if data == 'del_text':
            database.set_about(option='text')
            logger.info(f'Изменение секции\tcallbackData:\t{call.data}')
            await call.message.answer('Успешно!')
        elif data == 'del_photo':
            database.set_about(option='photo')
            logger.info(f'Изменение секции\tcallbackData:\t{call.data}')
            await call.message.answer('Успешно!')
        elif data == 'del_video':
            database.set_about(option='video')
            logger.info(f'Изменение секции\tcallbackData:\t{call.data}')
            await call.message.answer('Успешно!')
        elif data == 'del_document':
            database.set_about(option='document')
            logger.info(f'Изменение секции\tcallbackData:\t{call.data}')
            await call.message.answer('Успешно!')
        elif data == 'edit':
            await EditState.edit_about.set()
            await call.message.answer('Изменение секции "О нас"', reply_markup=edit_keyboard)

    except:
        logger.error(f'Ошибка изменения секции\tcallbackData:\t{call.data}')
        await call.message.answer('Ошибка')


@bot_dp.message_handler(text='Завершиить изменения', state=EditState.edit_about)
async def s(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('ОК', reply_markup=core_markup)


@bot_dp.message_handler(state=EditState.edit_about, content_types=['text'])
async def s(message: types.Message):
    logger.info('Изменение about text')
    database.set_about(option='text', content=message.text)
    await message.answer('ОК')


@bot_dp.message_handler(state=EditState.edit_about, content_types=['photo'])
async def s(message: types.Message):
    logger.info('Изменение about photo')
    pprint(dict(message))
    database.set_about(option='photo', content=message.photo[-1].file_id)
    await message.answer('ОК\n' + '\n\n'.join([file.file_id for file in message.photo]))


@bot_dp.message_handler(state=EditState.edit_about, content_types=['video'])
async def s(message: types.Message):
    logger.info('Изменение about video')
    database.set_about(option='video', content=message.video.file_id)
    await message.answer('ОК')


@bot_dp.message_handler(state=EditState.edit_about, content_types=['document'])
async def s(message: types.Message):
    logger.info('Изменение about document')
    database.set_about(option='document', content=message.document.file_id)
    await message.answer('ОК')
