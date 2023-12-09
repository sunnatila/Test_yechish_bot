from aiogram.dispatcher.filters.state import State, StatesGroup


class Signup(StatesGroup):
    phone = State()
    register = State()
    email = State()
    birthday = State()
    confirm = State()







