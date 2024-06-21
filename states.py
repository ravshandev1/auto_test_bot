from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    lang = State()
    name = State()
    phone_number = State()


class Feedback(StatesGroup):
    text = State()


class Subscribe(StatesGroup):
    rate = State()
    payment_type = State()
    checkout = State()
    success = State()
