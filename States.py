from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    admin = State()

    edit_about = State()
