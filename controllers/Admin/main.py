from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger
from configure import config
from pprint import pprint


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
        ).add(
            KeyboardButton('Статистика по подписчикам')
        ).add(
            KeyboardButton('Создания уведомления')
        )

@logger.catch()
def admin_controller(database):
    try:
        bot = Bot(config['bot_admin_token'])
        bot_dp = Dispatcher(bot)
        logger.info('Прошли верификацию admin bot token.')
    except:
        logger.error('Ошибка верификации admin bot token.')

    @bot_dp.message_handler(content_types=['text'])
    async def start(message: types.Message):
        '''
            Авторизация админа
            Просто недаём пройти функции дальше авторизации если авторизации ещё не было
            Можно было бы написать через декоратор, но, вроде, и так неплохо
        '''
        if message.text == config['admin_password']:
            database.add_admin(message)
            await message.answer('Авторизация успешна', reply_markup=core_markup)
            return None
        elif not database.is_admin(message):
            await message.answer('Введите пароль авторизации')
            return None

        ''' По отдельности обрабатываем все кновки на главной клаве '''
        if message.text == 'О нас':
            await standard_answer(message, database.get_about())
        elif message.text == 'Преподаватели':
            await standard_answer(message, database.get_teachers())
        elif message.text == 'Часто задаваемые вопросы':
            pass
        elif message.text == 'Цены':
            await standard_answer(message, database.get_prices())
        elif message.text == 'Расписание':
            await standard_answer(message, database.get_timetable())
        elif message.text == 'Возраст ребёнка':
            pass
        elif message.text == 'Статистика по подписчикам':
            pass
        elif message.text == 'Создания уведомления':
            pass


    return bot, bot_dp