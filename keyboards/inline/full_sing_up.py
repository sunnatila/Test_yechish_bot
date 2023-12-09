from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

yes_or_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Royhatdan otish", callback_data="yes")
        ]
    ]
)


