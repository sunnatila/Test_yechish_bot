from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from loader import dp, db, bot
from aiogram.dispatcher.filters import Command


@dp.message_handler(Command("set_email"))
async def set_email(msg: types.Message, state: FSMContext):
    await msg.answer("Emailingizni qaytadan kiriting: ")
    await state.set_state('email_send')


@dp.message_handler(state='email_send')
async def send_email(msg: types.Message, state: FSMContext):
    email = msg.text
    user_id = msg.from_user.id
    db.update_email(user_id, email)
    await msg.answer("Emailingiz muvaffaqiyatli ozgartirildi.")
    await state.finish()


@dp.message_handler(Command("set_number"))
async def set_email(msg: types.Message, state: FSMContext):
    await msg.answer("Nomeringizni qaytadan kiriting: ")
    await state.set_state('number_send')


@dp.message_handler(state='number_send')
async def send_email(msg: types.Message, state: FSMContext):
    number = msg.text
    user_id = msg.from_user.id
    db.update_number(user_id, number)
    await msg.answer("Nomeringiz muvaffaqiyatli ozgartirildi.")
    await state.finish()


@dp.message_handler(Command("set_fullname"))
async def set_email(msg: types.Message, state: FSMContext):
    await msg.answer("Ism-Familiyangizni qaytadan kiriting: ")
    await state.set_state('fullname_send')


@dp.message_handler(state='fullname_send')
async def send_email(msg: types.Message, state: FSMContext):
    fullname = msg.text
    user_id = msg.from_user.id
    db.update_fullname(user_id, fullname)
    await msg.answer("Ism-Familiyangiz muvaffaqiyatli ozgartirildi.")
    await state.finish()


@dp.message_handler(Command("set_birthday"))
async def set_email(msg: types.Message, state: FSMContext):
    await msg.answer("Tug'ilgan kuningizni qaytadan kiriting\n"
                     "Namuna 1-1-2001 yoki 1.1.2001: ")
    await state.set_state('birthday_send')


@dp.message_handler(state='birthday_send')
async def send_email(msg: types.Message, state: FSMContext):
    birthday = msg.text
    user_id = msg.from_user.id
    db.update_birthday(user_id, birthday)
    await msg.answer("Tug'ilgan kuningiz muvaffaqiyatli ozgartirildi.")
    await state.finish()

