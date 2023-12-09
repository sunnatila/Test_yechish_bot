from aiogram import types
from aiogram.dispatcher.filters import Command
from data.config import ADMINS
from loader import dp, db, bot
from states import Signup
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from keyboards.default.test_button import test
from keyboards.inline import tasdiqlash_yoki_yoq


@dp.message_handler(content_types="contact", is_sender_contact="True", state=Signup.phone)
async def phone_send(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    fullname = msg.from_user.full_name
    phone = msg.contact.phone_number
    db.add_user(user_id, fullname, phone)
    await msg.answer("Botdan foydalanishiz mumkun.", reply_markup=test)
    await state.finish()


@dp.callback_query_handler(text=("yes", 'yoq'), state=(Signup.register, Signup.confirm))
async def full_sign_up(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Emailingizni kiriting: ")
    await state.set_state(Signup.email)


@dp.message_handler(state=Signup.email)
async def email_send(msg: types.Message, state: FSMContext):
    email = msg.text
    await state.update_data({'email': email})
    await msg.answer("Tugilgan kuningizni kiriting "
                     "Namuna (1.1.2001 yoki 1-1-2001): ")
    await Signup.next()


@dp.message_handler(content_types=ContentType.ANY, state=Signup.register)
async def err_full_signup(msg: types.Message):
    await msg.answer("Iltimos ro'yxatdan o'tish uchun tugmani bosing!")


@dp.message_handler(state=Signup.birthday)
async def email_send(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    birthday = msg.text
    email = await state.get_data('email')
    db.add_email_birthday(user_id, f'{email}', f'{birthday}')
    user = db.select_user(user_id)
    email_user = await state.get_data('email')
    info = "Sizning malumotlaringiz\n"
    info += f"Ism-Familiyangiz: {user[1]}\n"
    info += f"Nomeringiz: {user[2]}\n"
    info += f"Emailingiz: {email_user.get('email')}\n"
    info += f"Tugilgan kuningiz: {user[4]}\n"
    await msg.answer(f"{info}", reply_markup=tasdiqlash_yoki_yoq)
    await Signup.next()


@dp.callback_query_handler(text="ha", state=Signup.confirm)
async def tasdiqlash(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user = db.select_user(user_id)
    info = "Ro'yxatdan o'tgan odam\n"
    info += f"id: {user[0]}\n"
    info += f"Fullname: {user[1]}\n"
    info += f"Phone number: {user[2]}\n"
    info += f"Email: {user[3]}\n"
    info += f"Birthday: {user[4]}\n"
    await call.answer("Ma'lumotlaringiz muvaffaqqiyatli saqlandi!", show_alert=True)
    await call.message.answer("Test yechish tugmasini bosing", reply_markup=test)
    await call.message.delete()
    await bot.send_message(ADMINS[0], info)
    await state.finish()


@dp.message_handler(Command('info'))
async def user_info(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    user = db.select_user(user_id)
    email_user = await state.get_data('email')
    info = "Sizning malumotlaringiz\n"
    info += f"Fullname: {user[1]}\n"
    info += f"Phone number: {user[2]}\n"
    info += f"Email: {email_user.get('email')}\n"
    info += f"Birthday: {user[4]}\n"
    await msg.reply(info)
