from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from DataBase.main import database

questions = database.telegram_bot.content.find_one({'_id': 'faq'})['content']

faq_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(questions[i]['question'], callback_data='faq:' + str(i))] for i in range(len(questions))]
)


def get_answer(index: int) -> dict:
    return questions[index]['answer']

