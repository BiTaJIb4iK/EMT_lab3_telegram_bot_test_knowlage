import asyncio
import logging
import sys
import random
from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, BotCommandScopeDefault, CallbackQuery, ContentType
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.DataTypes.dbtypes import Answers

def getStartKeyboard(d :Answers):
    keyboard_builder = InlineKeyboardBuilder()

    #pack Buttons
    keyboard_builder.button(text="Start test", callback_data=d.pack())

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()

def getQuizKeyboard(d :Answers, q):
    keyboard_builder = InlineKeyboardBuilder()

    #pack Buttons
    keyboard_builder.button(text=q[3], callback_data=Answers(current_question=d.current_question, current_test_id=d.current_test_id, previous_answer=1).pack())
    keyboard_builder.button(text=q[4], callback_data=Answers(current_question=d.current_question, current_test_id=d.current_test_id, previous_answer=2).pack())
    keyboard_builder.button(text=q[5], callback_data=Answers(current_question=d.current_question, current_test_id=d.current_test_id, previous_answer=3).pack())
    keyboard_builder.button(text=q[6], callback_data=Answers(current_question=d.current_question, current_test_id=d.current_test_id, previous_answer=4).pack())

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()

