from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

test_ga_ruhsat = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Saqlash", callback_data="saqlash"),
            InlineKeyboardButton(text="Tahrirlash", callback_data="yoq"),
        ]
    ], row_width=2
)




