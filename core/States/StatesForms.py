from aiogram.fsm.state import StatesGroup, State

class StateForm(StatesGroup):
    GET_QUESTION = State()
    GET_ANSWER1 = State()
    GET_ANSWER2 = State()
    GET_ANSWER3 = State()
    GET_ANSWER4 = State()
    GET_RIGHT_ANSWER = State()