from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

core_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('О нас')
).add(
    KeyboardButton('Преподаватели')
).add(
    KeyboardButton('Цены')
).add(
    KeyboardButton('Расписание')
).add(
    KeyboardButton('Часто задаваемые вопросы')
).add(
    KeyboardButton('Статистика по подписчикам')
).add(
    KeyboardButton('Создания уведомления')
)

