from aiogram.filters.callback_data import CallbackData
from dataclasses import dataclass
from typing import List

class Answers(CallbackData, prefix="quiz"):
    current_question: int
    current_test_id: int
    previous_answer: int
