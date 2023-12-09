from aiogram.dispatcher.filters.state import StatesGroup, State


class TestYechishStateGroup(StatesGroup):
    success = State()
    yechilmoqda = State()