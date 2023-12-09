import asyncio
import sqlite3
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BadRequest

from keyboards.inline import test_ga_ruhsat
from states import TestState
from data.config import ADMINS
from loader import dp, db
from keyboards.default import otqazvorish, add_test_or_view_tests
from aiogram.types import ContentType, ReplyKeyboardRemove


@dp.message_handler(text="Test qoshish", chat_id=ADMINS)
async def send_test(msg: types.Message, state: FSMContext):
    await msg.answer("Rasm kiriting, rasimingiz yoq bolsa otqazvorish tugmasini bosing.", reply_markup=otqazvorish)
    await state.set_state(TestState.photo)


@dp.message_handler(content_types=(ContentType.PHOTO, ContentType.DOCUMENT), state=TestState.photo)
async def send_photo(msg: types.Message, state: FSMContext):
    if msg.photo:
        doc_id = msg.photo[-1].file_id
    else:
        doc_id = msg.document.file_id
    await state.update_data({'doc_id': doc_id})
    await msg.answer("Test shartini kiriting (majburiy): ", reply_markup=ReplyKeyboardRemove())
    await TestState.next()


@dp.message_handler(text="Otqazvorish", state=TestState.photo, chat_id=ADMINS)
async def con(msg: types.Message):
    await msg.answer("Savolni kiriting(majburiy): ")
    await TestState.next()


@dp.message_handler(content_types=ContentType.ANY, state=TestState.photo)
async def error_photo(msg: types.Message):
    await msg.answer("Rasm yuboring yoki o'tkazib yuborish tugmasini bosing!", reply_markup=otqazvorish)


@dp.message_handler(state=TestState.questions, chat_id=ADMINS)
async def send_questions(msg: types.Message, state: FSMContext):
    savol = msg.text
    await state.update_data({'questions': savol})
    await msg.answer("Variant 1 ni kiriting: ")
    await TestState.next()


@dp.message_handler(state=TestState.variant1, chat_id=ADMINS)
async def variant(msg: types.Message, state: FSMContext):
    variant1 = msg.text
    await state.update_data({'variant1': variant1})
    await msg.answer("Variant 2 ni kiriting: ")
    await TestState.next()


@dp.message_handler(state=TestState.variant2, chat_id=ADMINS)
async def variant2(msg: types.Message, state: FSMContext):
    var2 = msg.text
    await state.update_data({'variant2': var2})
    await msg.answer("Variant 3 ni kiriting: ")
    await TestState.next()


@dp.message_handler(state=TestState.variant3, chat_id=ADMINS)
async def variant3(msg: types.Message, state: FSMContext):
    var3 = msg.text
    await state.update_data({'variant3': var3})
    await msg.answer("Variant 4 ni kiriting: ")
    await TestState.next()


@dp.message_handler(state=TestState.variant4)
async def send_four_response(msg: types.Message, state: FSMContext):
    await state.update_data({'variant4': msg.text})
    info = f"Test {datetime.now().date()} {datetime.now().strftime('%X')}:\n"
    async with state.proxy() as data:
        try:
            photo_id = data['doc_id']
        except KeyError:
            photo_id = None
        question = data['questions']
        response = data['variant1']
        response1 = data['variant2']
        response2 = data['variant3']
        response3 = data['variant4']
    info += f"Savol:\n" \
            f"{question}\n" \
            f"variant1*: {response}\n" \
            f"variant2: {response1}\n" \
            f"variant3: {response2}\n" \
            f"variant4: {response3}\n"
    if photo_id:
        try:
            await msg.answer_photo(photo_id, caption=info, reply_markup=test_ga_ruhsat)
        except BadRequest:
            await msg.answer_document(photo_id, caption=info, reply_markup=test_ga_ruhsat)
    else:
        await msg.answer(info, reply_markup=test_ga_ruhsat)
    await TestState.next()


@dp.callback_query_handler(text='saqlash', state=TestState.confirm)
async def confirm_true(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        try:
            photo_id = data['doc_id']
        except KeyError:
            photo_id = None
        question = data['questions']
        response = data['variant1']
        response1 = data['variant2']
        response2 = data['variant3']
        response3 = data['variant4']
    try:
        db.add_test(question, response, response1, response2, response3, photo_id)
    except sqlite3.IntegrityError:
        await call.message.delete()
        await call.message.answer("Bunday savol mavjud qayta kiriting:", reply_markup=add_test_or_view_tests)
        await state.finish()
        return
    await call.message.answer("Kategoriyani tanlang", reply_markup=add_test_or_view_tests)
    await call.answer("Test muvaffaqiyatli saqlandi!", show_alert=True)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text='yoq', state=TestState.confirm)
async def confirm_true(call: types.CallbackQuery):
    await call.answer("Qayta ma'lumotlarni kiriting!")
    await call.message.delete()
    await call.message.answer("Testning rasmi bo'lsa rasmni yuboring aks holda o'tkazib yuborish tugmasini bosing!", reply_markup=otqazvorish)
    await TestState.photo.set()


@dp.message_handler(content_types=ContentType.ANY, state=TestState.confirm)
async def any_message(msg: types.Message):
    await msg.answer("Test to'g'ri ekanligini tasdiqlang!")


@dp.message_handler(text="Testlarni korish", user_id=ADMINS)
async def add_test(msg: types.Message):
    tests = db.select_tests()
    count = db.select_count_tests()
    for test in tests:
        info = f"Test {test[6]}:\n"
        info += f"Savol:\n" \
                f"{test[1]}\n" \
                f"variant1*: {test[2]}\n" \
                f"variant2: {test[3]}\n" \
                f"variant3: {test[4]}\n" \
                f"variant4: {test[5]}\n"
        try:
            await msg.answer_photo(test[0], caption=info)
        except BadRequest:
            try:
                await msg.answer_document(test[0], caption=info)
            except BadRequest:
                await msg.answer(info)
        await asyncio.sleep(0.05)
    await msg.answer(f"Testlar soni: {count}")

