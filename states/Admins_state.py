from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminState(StatesGroup):
    post = State()
    post_send = State()


