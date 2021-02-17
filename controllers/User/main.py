from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from loguru import logger
from configure import config
from controllers.User.childs_age import choice_age_keyboard
from controllers.User.faq import faq_keyboard, questions, get_answer
from pprint import pprint


core_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton('О нас')
        ).add(
            KeyboardButton('Преподаватели')
        ).add(
            KeyboardButton('Часто задаваемые вопросы')
        ).add(
            KeyboardButton('Цены')
        ).add(
            KeyboardButton('Расписание')
        ).add(
            KeyboardButton('Возраст ребёнка')
        )


async def standard_answer(message, content):
    if content['text']:
        await message.answer(content['text'], reply_markup=core_markup)

    if content['photo']:
        await message.answer_photo(content['photo'])

    if content['video']:
        await message.answer_video(content['video'])

    if content['document']:
        await message.answer_document(content['document'])

    if content['voice']:
        await message.answer_voice(content['voice'])


@logger.catch()
def user_controller(database):
    try:
        bot = Bot(config['bot_token'])
        bot_dp = Dispatcher(bot)
        logger.info('Прошли верификацию bot token.')
    except:
        logger.error('Ошибка верификации bot token.')

    @bot_dp.message_handler(commands=['start'])
    async def start(message: types.Message):

        # Всех пользователей заносим в БД
        database.registration_user(message)

        await standard_answer(message, database.get_hello())

    @bot_dp.message_handler(text='О нас')
    async def about(message: types.Message):
        await standard_answer(message, database.get_about())

    @bot_dp.message_handler(text='Преподаватели')
    async def teachers(message: types.Message):
        await standard_answer(message, database.get_teachers())

    @bot_dp.message_handler(text='Цены')
    async def prices(message: types.Message):
        await standard_answer(message, database.get_prices())

    @bot_dp.message_handler(text='Расписание')
    async def timetable(message: types.Message):
        await standard_answer(message, database.get_timetable())

    @bot_dp.message_handler(text='Возраст ребёнка')
    async def childs_age(message: types.Message):
        await message.answer('Выберете возраст', reply_markup=choice_age_keyboard)

    @bot_dp.callback_query_handler(text_contains='age')
    async def callback_choice_age(call: CallbackQuery):
        database.edit_age_group(chat_id=call.message.chat.id, value=call.data.split(':')[1])
        await call.message.answer('Возраст успешно обновлён!!!')

    @bot_dp.message_handler(text='Часто задаваемые вопросы')
    async def faq(message: types.Message):
        await message.answer('FAQ', reply_markup=faq_keyboard)

    @bot_dp.callback_query_handler(text_contains='faq')
    async def callback_choice_age(call: CallbackQuery):
        await standard_answer(call.message, get_answer(int(call.data.split(':')[1])))

    return bot, bot_dp
