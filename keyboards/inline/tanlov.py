from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


tasdiqlash_yoki_yoq = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Tasdiqlash", callback_data="ha"),
            InlineKeyboardButton(text="Ozgartirish", callback_data="yoq")
        ]
    ],
    row_width=2
)



