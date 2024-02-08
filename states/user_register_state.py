from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    # id = State() 
    phone_number = State()
    FIO = State()
    # city = State()