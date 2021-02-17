from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

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



