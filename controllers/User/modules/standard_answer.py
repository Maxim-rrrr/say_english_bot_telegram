from aiogram.types import ReplyKeyboardMarkup,  InlineKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from aiogram import types
from loguru import logger
import typing


@logger.catch()
async def standard_answer(
        message: types.Message,
        content: dict,
        markup: typing.Union[
            InlineKeyboardMarkup,
            ReplyKeyboardMarkup,
            ReplyKeyboardRemove,
            ForceReply,
            None,
        ] = None):

    if content['text']:
        await message.answer(content['text'], reply_markup=markup)

    if content['photo']:
        await message.answer_photo(content['photo'], reply_markup=markup)

    if content['video']:
        await message.answer_video(content['video'], reply_markup=markup)

    if content['document']:
        await message.answer_document(content['document'], reply_markup=markup)

    if content['voice']:
        await message.answer_voice(content['voice'], reply_markup=markup)
