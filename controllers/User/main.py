from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import ValidationError
from loguru import logger

from configure import config

try:
    bot = Bot(config['bot_token'])
    bot_dp = Dispatcher(bot)
    logger.info('Прошли верификацию bot token.')
except ValidationError:
    logger.error('Ошибка верификации bot token.')

'''
    Команда start просто возвращает приветственное сообщение из бд
'''
import controllers.User.modules.command_start

'''
    По отдельности обрабатываем все кнопки на главной клаве 
    - 'О нас'
    - 'Преподаватели'
    - 'Часто задаваемые вопросы'
    - 'Цены'
    - 'Расписание'
    - 'Возраст ребёнка'
'''
import controllers.User.modules.about
import controllers.User.modules.teachers
import controllers.User.modules.faq
import controllers.User.modules.prices
import controllers.User.modules.timetable
import controllers.User.modules.childs_age



