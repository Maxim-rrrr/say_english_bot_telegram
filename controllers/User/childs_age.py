from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from controllers.bot import bot_dp
from DataBase.main import database

age_callback = CallbackData('age', 'type_group')

groups = [
    '6-8',
    '9-11',
    '12-14',
    '15-18',
    '18+'
]

choice_age_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(f'{group} лет', callback_data=age_callback.new(type_group=group))] for group in groups
    ]
)


@bot_dp.message_handler(text='Возраст ребёнка')
async def childs_age(message: types.Message):
    await message.answer('Выберете возраст', reply_markup=choice_age_keyboard)


@bot_dp.callback_query_handler(text_contains='age')
async def callback_choice_age(call: CallbackQuery):
    database.edit_age_group(chat_id=call.message.chat.id, value=call.data.split(':')[1])
    await call.message.answer('Возраст успешно обновлён!!!')
