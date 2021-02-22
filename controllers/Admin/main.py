from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import ValidationError
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from loguru import logger

from configure import config

try:
    bot = Bot(config['bot_admin_token'])
    bot_dp = Dispatcher(bot, storage=MemoryStorage())
    logger.info('Прошли верификацию admin bot token.')
except ValidationError:
    logger.error('Ошибка верификации admin bot token.')

'''
    Принимает пароль от пользователя и проводит авторизацию
'''
import controllers.Admin.modules.auth


'''
    Команда start просто прокидывает проверку на админа и в случае, 
    если пользователь не авторизован просит ввести пароль 
'''
import controllers.Admin.modules.command_start


''' 
    По отдельности обрабатываем все кнопки на главной клаве 
    - 'О нас'                       TODO
    - 'Преподаватели'               TODO
    - 'Цены'                        TODO
    - 'Расписание'                  TODO
    - 'Часто задаваемые вопросы'    TODO
    - 'Статистика по подписчикам'   TODO
    - 'Создания уведомления'        TODO
'''

import controllers.Admin.modules.about
import controllers.Admin.modules.teachers
import controllers.Admin.modules.prices
import controllers.Admin.modules.timetable
import controllers.Admin.modules.faq

