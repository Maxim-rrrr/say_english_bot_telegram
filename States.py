from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    admin = State()

    about = State()
    teachers = State()
    prices = State()
    timetable = State()
    start = State()

    faq_add = State()