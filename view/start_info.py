"""
    Данный модуль отвечает за функцию отвечающую на команду /start
"""


def start_info(db, bot, chat_id):
    Content = db.content

    text = Content.find_one({'_id': 'start_info'})['text']
    bot.send_message(chat_id, text)
