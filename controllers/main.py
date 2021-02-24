from aiogram import types
from controllers.User.core_markup import core_markup
from States import States
from controllers.standard_section import standard_section
from config import config
from controllers.Admin.admin_markup import admin_markup
from controllers.bot import bot_dp

standard_section('О нас', States.about)
standard_section('Преподаватели', States.teachers)
standard_section('Цены', States.prices)
standard_section('Расписание', States.timetable)

standard_section('/start', States.start, core_markup)


import controllers.Admin.logout

import controllers.User.childs_age

import controllers.User.faq
import controllers.Admin.faq
import controllers.Admin.create_event

# Авторизацию прокидываем прям тут, а дальше всё через state
@bot_dp.message_handler(text=[config['admin_password']])
async def auth(message: types.Message):
    await States.admin.set()
    await message.answer('Авторизация успешна', reply_markup=admin_markup)
