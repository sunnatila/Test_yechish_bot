from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

tayorgarli = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Tayyorman", callback_data='tayorman')
        ],
    ],
    row_width=1
)
