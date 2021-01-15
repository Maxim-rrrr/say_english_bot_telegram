"""
    Данный модуль отвечает за функцию отвечающую на команду /start
"""
from loguru import logger


@logger.catch
async def start_info(db, message):
    Content = db.content

    text = Content.find_one({'_id': 'start_info'})['text']
    await message.answer(text)
