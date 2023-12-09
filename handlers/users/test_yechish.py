import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from data.config import ADMINS
from keyboards.default import test
from keyboards.inline import test_ga_ruhsat, yes_or_no, tayorgarli, variants_buttons
from loader import dp, db, bot
from states import Signup, TestYechishStateGroup


@dp.message_handler(text="Test yechish")
async def solution_test(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    user = db.select_user(user_id)
    if user[3] is None:
        await msg.answer("To'liq ro'yxatdan o'tish!", reply_markup=ReplyKeyboardRemove())
        await msg.answer("Test yechish uchun email va tug'ilgan kuningizni kiriting:", reply_markup=yes_or_no)
        await state.set_state(Signup.register)
    else:
        await msg.answer("Test yechishni boshlang!", reply_markup=ReplyKeyboardRemove())
        await msg.answer("Tayyormisiz?", reply_markup=tayorgarli)
        await TestYechishStateGroup.success.set()


@dp.callback_query_handler(text="tayorman", state=TestYechishStateGroup.success)
async def success_test(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_id = call.from_user.id
    user = db.select_user(user_id)
    if user[5] > 1:
        await call.message.answer("Boshqa test yechishga ruxsat yo'q!")
        await state.finish()
        return
    urinish = user[5] + 1
    db.update_urinish(user_id, urinish)
    all_tests = db.select_tests()
    try:
        test_10 = random.sample(all_tests, 10)
    except ValueError:
        test_10 = random.sample(all_tests, len(all_tests))
    if len(test_10) == 0:
        await call.message.answer(f"Bazada test mavjud emas!", reply_markup=test)
        await state.finish()
        return
    test1 = random.choice(test_10)
    test_10.remove(test1)
    await state.update_data({'tests': test_10, 'count': 0})
    try:
        await call.message.answer_photo(test1[1], caption=test1[6], reply_markup=variants_buttons(test1))
    except BadRequest:
        try:
            await call.message.answer_document(test1[1], caption=test1[6], reply_markup=variants_buttons(test1))
        except BadRequest:
            await call.message.answer(test1[0], reply_markup=variants_buttons(test1))
    await TestYechishStateGroup.next()


@dp.message_handler(content_types=ContentType.ANY, state=TestYechishStateGroup.success)
async def check_button(msg: types.Message):
    await msg.answer("Testni boshlash uchun Tayyorman tugmani bosing!")


@dp.callback_query_handler(text='true', state=TestYechishStateGroup.yechilmoqda)
async def test_yechish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    count = data.get('count')
    test_10 = data.get('tests')
    count += 1
    await state.update_data({'count': count})
    if len(test_10) == 0:
        await call.message.answer(f"{count} ta testni to'g'ri topdingiz!", reply_markup=test)
        await bot.send_message(ADMINS[0], f"{call.from_user.full_name} {count}ta testni topdi!")
        await state.finish()
        return
    test1 = random.choice(test_10)
    test_10.remove(test1)
    await state.update_data({'tests': test_10})
    try:
        await call.message.answer_photo(test1[1], caption=test1[0], reply_markup=variants_buttons(test1))
    except BadRequest:
        try:
            await call.message.answer_document(test1[1], caption=test1[0], reply_markup=variants_buttons(test1))
        except BadRequest:
            await call.message.answer(test1[0], reply_markup=variants_buttons(test1))


@dp.callback_query_handler(text='false', state=TestYechishStateGroup.yechilmoqda)
async def test_yechish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    count = await state.get_data('count')
    test_10 = data.get('tests')
    if len(test_10) == 0:
        await call.message.answer(f"{count.get('count')} ta testni to'g'ri topdingiz!", reply_markup=test)
        await bot.send_message(ADMINS[0], f"{call.from_user.full_name} {count.get('count')}ta testni topdi!")
        await state.finish()
        return
    test1 = random.choice(test_10)
    test_10.remove(test1)
    await state.update_data({'tests': test_10})
    try:
        await call.message.answer_photo(test1[1], caption=test1[0], reply_markup=variants_buttons(test1))
    except BadRequest:
        try:
            await call.message.answer_document(test1[1], caption=test1[0], reply_markup=variants_buttons(test1))
        except BadRequest:
            await call.message.answer(test1[0], reply_markup=variants_buttons(test1))
