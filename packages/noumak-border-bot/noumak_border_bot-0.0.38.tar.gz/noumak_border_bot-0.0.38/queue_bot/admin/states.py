from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    text_mailing = State()
    admin_add = State()
