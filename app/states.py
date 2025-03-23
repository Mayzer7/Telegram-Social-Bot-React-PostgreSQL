from aiogram.fsm.state import StatesGroup, State  

class WritePost(StatesGroup):
    waiting_for_text = State()