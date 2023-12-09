from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default import Kontakt, add_test_or_view_tests, test
from states import Signup
from loader import dp, db


@dp.message_handler(CommandStart(), user_id=ADMINS)
async def bot_start(message: types.Message):
    await message.answer("Bot qayta ishga tushdi!", reply_markup=add_test_or_view_tests)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    ids = db.select_users_ids()
    user_id = message.from_user.id
    if user_id in ids:
        await message.answer("Bot qayta ishga tushdi!", reply_markup=test)
        return
    await message.answer(f"Salom, {message.from_user.full_name}\n"
                         f"Botdan foydalanish uchun ro'yxatdan o'ting: ", reply_markup=Kontakt)
    await state.set_state(Signup.phone)
