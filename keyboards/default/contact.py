from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

Kontakt = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kontaktni yuborish", request_contact=True),
        ],
    ],
    resize_keyboard=True
)


