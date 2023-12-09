from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from data.config import ADMINS
from keyboards.inline.post_send import post_or_no
from loader import dp, db, bot
from aiogram.dispatcher.filters import Command

from states import AdminState


@dp.message_handler(Command("del_users"), user_id=ADMINS)
async def del_users(msg: types.Message):
    db.del_users()
    await msg.answer("Foydalanuvchilar ochirildi!")


@dp.message_handler(Command("all_users"), user_id=ADMINS)
async def del_users(msg: types.Message):
    users = db.select_users()
    for user in users:
        await msg.answer(f"User_id: {user[0]} \nFullname: {user[1]} \nPhone number: {user[2]} \nEmail: {user[3]}\n"
                         f"Birthday: {user[4]}\n")


@dp.message_handler(Command("send_post"), user_id=ADMINS)
async def post_admin(msg: types.Message, state: FSMContext):
    await msg.reply("Post kiriting:")
    await state.set_state(AdminState.post)


@dp.message_handler(state=AdminState.post, user_id=ADMINS)
async def post_waiting(msg: types.Message, state: FSMContext):
    post = msg.text
    info = "Postni hamma foydalanuvchilarga yuborishni tasdilaysizmi?\n"
    info += f"Post: {post}"
    await state.update_data({'post': post})
    await msg.answer(info, reply_markup=post_or_no)
    await AdminState.next()


@dp.callback_query_handler(text="tasdiqlash", state=AdminState.post_send, user_id=ADMINS)
async def send_a_post(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    post = await state.get_data('post')
    post_yes = post.get('post')
    users_id = db.select_users_ids()
    for user in users_id:
        await bot.send_message(user, post_yes)
    await call.message.answer("Post hama foydalanuvchilarga yuborildi.✔️")
    await state.finish()


@dp.callback_query_handler(text="rad_etish", state=AdminState.post_send, user_id=ADMINS)
async def refuse_to_post(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Post rad etildi.")
    await state.finish()


@dp.message_handler(Command('del_tests'))
async def del_tests(msg: types.Message):
    db.del_tests()
    await msg.answer("Testlar ochirildi.")



@dp.message_handler(state=AdminState.post, user_id=ADMINS)
async def post_waiting(msg: types.Message, state: FSMContext):
    post = msg.text
    info = "Postni hamma foydalanuvchilarga yuborishni tasdilaysizmi?\n"
    info += f"Post: {post}"
    await state.update_data({'post': post})
    await msg.answer(info, reply_markup=post_or_no)
    await AdminState.next()



