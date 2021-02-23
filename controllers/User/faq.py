from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from controllers.bot import bot_dp
from DataBase.main import database


@bot_dp.message_handler(text='Часто задаваемые вопросы')
async def faq(message: types.Message):
    questions = database.get('faq')
    faq_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(questions[i]['question'], callback_data='faq:' + str(i))] for i in
                         range(len(questions))]
    )
    await message.answer('FAQ', reply_markup=faq_keyboard)


@bot_dp.callback_query_handler(text_contains='faq')
async def callback_choice_faq(call: CallbackQuery):
    questions = database.get('faq')
    index = int(call.data.split(':')[1])
    await call.message.answer(questions[index]['answer'])
