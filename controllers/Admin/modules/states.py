from aiogram.dispatcher.filters.state import StatesGroup, State


class EditState(StatesGroup):
    edit_about = State()
