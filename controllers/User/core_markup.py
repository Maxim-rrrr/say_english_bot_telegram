from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


Standard_section = ['О нас', 'Преподаватели', 'Цены', 'Расписание']

core_markup = ReplyKeyboardMarkup(resize_keyboard=True)

for section in Standard_section:
    core_markup.add(section)

core_markup.add(
    KeyboardButton('Часто задаваемые вопросы')
).add(
    KeyboardButton('Возраст ребёнка')
)
