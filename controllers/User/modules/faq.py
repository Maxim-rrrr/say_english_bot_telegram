from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from controllers.User.main import bot_dp
from DataBase.main import database
from controllers.User.modules.standard_answer import standard_answer


questions = database.telegram_bot.content.find_one({'_id': 'faq'})['content']

faq_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(questions[i]['question'], callback_data='faq:' + str(i))] for i in
                     range(len(questions))]
)


def get_answer(index: int) -> dict:
    return questions[index]['answer']


@bot_dp.message_handler(text='Часто задаваемые вопросы')
async def faq(message: types.Message):
    await message.answer('FAQ', reply_markup=faq_keyboard)


@bot_dp.callback_query_handler(text_contains='faq')
async def callback_choice_faq(call: CallbackQuery):
    await standard_answer(call.message, get_answer(int(call.data.split(':')[1])))
