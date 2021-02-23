from aiogram import types
from aiogram.dispatcher import FSMContext

from controllers.bot import bot_dp
from States import States
from controllers.User.core_markup import core_markup


@bot_dp.message_handler(text='Выйти из админки', state=States.admin)
async def admin_get(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Выход', reply_markup=core_markup)