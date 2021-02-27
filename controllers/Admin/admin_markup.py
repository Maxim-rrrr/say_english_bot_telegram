from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


Standard_section = ['О нас', 'Преподаватели', 'Цены', 'Расписание', '/start']

admin_markup = ReplyKeyboardMarkup(resize_keyboard=True)

for section in Standard_section:
    admin_markup.add(section)

admin_markup.add(
    KeyboardButton('Часто задаваемые вопросы')
).add(
    KeyboardButton('Статистика')
).add(
    KeyboardButton('Уведомления')
).add(
    KeyboardButton('Выйти из админки')
)

