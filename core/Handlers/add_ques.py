import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, BotCommandScopeDefault, CallbackQuery, ContentType
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from datetime import datetime

from core.Keyboards.general import getMainMenuKeyboard, getProfileKeyboard
from core.Database.user import addUser, checkValidUser, getUser, isUserAdmin
from core.Database.debug import selectTable
from core.Database.questions import getQuizHistory, getQuestionsCount, createQuestion
from core.States.StatesForms import StateForm
from aiogram.fsm.context import FSMContext

temp_question: dict[int, list[int, int, str, str, str, str, str]] = {}

async def enterQuestion(message: types.Message, state: FSMContext) -> None:
    temp_question[message.chat.id] = [0, 0, '', '', '', '', '']
    temp_question[message.chat.id][0] = getQuestionsCount() + 1
    temp_question[message.chat.id][2] = message.text
    await state.set_state(StateForm.GET_ANSWER1)
    await message.answer("Enter answer 1 : \n")


async def enterAnswer1(message: types.Message, state: FSMContext) -> None:
    temp_question[message.chat.id][3] = message.text
    await state.set_state(StateForm.GET_ANSWER2)
    await message.answer("Enter answer 2 : \n")


async def enterAnswer2(message: types.Message, state: FSMContext) -> None:
    temp_question[message.chat.id][4] = message.text
    await state.set_state(StateForm.GET_ANSWER3)
    await message.answer("Enter answer 3 : \n")


async def enterAnswer3(message: types.Message, state: FSMContext) -> None:
    temp_question[message.chat.id][5] = message.text
    await state.set_state(StateForm.GET_ANSWER4)
    await message.answer("Enter answer 4 : \n")


async def enterRightAnswer(message: types.Message, state: FSMContext) -> None:
    temp_question[message.chat.id][6] = message.text
    await state.set_state(StateForm.GET_RIGHT_ANSWER)
    await message.answer("Enter Right Answer (1-4) : \n")


async def getRightAnswer(message: types.Message, state: FSMContext) -> None:
    temp_question[message.chat.id][1] = message.text
    createQuestion(temp_question[message.chat.id])
    await state.clear()
    await message.answer("Question added succesfully\n")