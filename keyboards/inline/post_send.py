from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


post_or_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Postni tasdiqlash", callback_data='tasdiqlash'),
            InlineKeyboardButton(text="Rad etish", callback_data="rad_etish"),
        ]
    ],
    row_width=2
)




