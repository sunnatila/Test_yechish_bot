from aiogram.dispatcher.filters.state import State, StatesGroup


class TestState(StatesGroup):
    photo = State()
    questions = State()
    variant1 = State()
    variant2 = State()
    variant3 = State()
    variant4 = State()
    confirm = State()


