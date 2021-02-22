from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from controllers.bot import bot_dp
from DataBase.main import database

age_callback = CallbackData('age', 'type_group')

choice_age_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('6-8 лет', callback_data=age_callback.new(type_group='6-8'))],
        [InlineKeyboardButton('9-11 лет', callback_data=age_callback.new(type_group='9-11'))],
        [InlineKeyboardButton('12-14 лет', callback_data=age_callback.new(type_group='12-14'))],
        [InlineKeyboardButton('15-18 лет', callback_data=age_callback.new(type_group='15-18'))],
        [InlineKeyboardButton('18+ лет', callback_data=age_callback.new(type_group='18+'))]
    ]
)


@bot_dp.message_handler(text='Возраст ребёнка')
async def childs_age(message: types.Message):
    await message.answer('Выберете возраст', reply_markup=choice_age_keyboard)


@bot_dp.callback_query_handler(text_contains='age')
async def callback_choice_age(call: CallbackQuery):
    database.edit_age_group(chat_id=call.message.chat.id, value=call.data.split(':')[1])
    await call.message.answer('Возраст успешно обновлён!!!')
