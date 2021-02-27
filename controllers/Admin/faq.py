from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,  InlineKeyboardMarkup, \
    ReplyKeyboardRemove, ForceReply, InlineKeyboardButton, CallbackQuery

from pprint import pprint

from controllers.bot import bot_dp
from States import States
from DataBase.main import database
from controllers.Admin.admin_markup import admin_markup

questions = database.get('faq')


async def send_faq(message: types.Message):
    for question in questions:
        index = questions.index(question)
        options_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    # InlineKeyboardButton('Изменить', callback_data=f'faq:edit:{index}'),
                    InlineKeyboardButton('Удалить', callback_data=f'faq:del:{index}')
                ]
            ]
        )

        await message.answer(
            f'Вопрос:\n{question["question"]}\n\nОтвет:\n{question["answer"]}',
            reply_markup=options_keyboard
        )

    options_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Добавить', callback_data=f'faq:add')
            ]
        ]
    )

    await message.answer(
        'Добавить вопрос',
        reply_markup=options_keyboard
    )


@bot_dp.message_handler(text='Часто задаваемые вопросы', state=States.admin)
async def faq(message: types.Message):
    await send_faq(message)


@bot_dp.callback_query_handler(text_contains='faq', state=States.admin)
async def callback(call: CallbackQuery):
    data = call.data.split(':')
    if data[1] == 'del':
        global questions
        del questions[int(data[2])]
        database.telegram_bot.content.update_one({'_id': 'faq'}, {'$set': {'content': questions}})
        await call.message.answer('OK')

        await send_faq(call.message)

    elif data[1] == 'edit':
        # TODO: Переход в состояние изменение КОНКРЕТНОГО вопроса
        pass
    elif data[1] == 'add':
        edit_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton('Отмена')
        )

        await States.faq_add.set()
        await call.message.answer(f'Напишите сообщение в формате:\n<Вопрос>\n\n<Ответ>', reply_markup=edit_keyboard)


@bot_dp.message_handler(text='Отмена', state=States.faq_add)
async def s(message: types.Message):
    await States.admin.set()
    await message.answer('ОК', reply_markup=admin_markup)


@bot_dp.message_handler(content_types=['text'], state=States.faq_add)
async def s(message: types.Message):
    content = message.text.split('\n\n')
    if len(content) == 2:
        global questions
        questions.append(
            {
                'question': content[0],
                'answer': content[1]
            }
        )
        database.telegram_bot.content.update_one({'_id': 'faq'}, {'$set': {'content': questions}})

        await States.admin.set()
        await message.answer('ОК', reply_markup=admin_markup)
        await send_faq(message)
    else:
        await message.answer(f'Напишите сообщение в формате\n<Вопрос>\n\n<Ответ>')






