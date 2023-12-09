import asyncio
import logging
import sys
from dataclasses import dataclass

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, BotCommandScopeDefault, CallbackQuery, ContentType
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from datetime import datetime
import random
from typing import List

from core.Keyboards.general import getMainMenuKeyboard
from core.Keyboards.quiz import getStartKeyboard, getQuizKeyboard
from core.Database.user import addUser, checkValidUser, getUser
from core.Database.debug import selectTable
from core.DataTypes.dbtypes import Answers
from core.Database.questions import getQuestionsCount, getQuestion, createQuiz, getQuizQuestion, updateToRightAnswer

previous_sent_message: int = {}


async def start_quiz(call: CallbackQuery, bot: Bot) -> None:
    Qcount = getQuestionsCount()

    if(Qcount<10):
        logging.ERROR("Not enought questions to start quiz!")
    
    questions = list(range(1, Qcount + 1))

    random.shuffle(questions)

    questions = questions[:10]
    
    questions.sort()
    print(questions)

    test_id = createQuiz(questions, call.from_user.id)

    a = Answers(current_question=1, current_test_id=test_id, previous_answer = 0)

    sent_mes = await call.message.answer("Are you ready to start the test?", reply_markup=getStartKeyboard(d=a))

    previous_sent_message[call.message.chat.id] = sent_mes.message_id

    await call.answer()



async def answerQuestion(call: CallbackQuery, bot: Bot) -> None:
    d = Answers.unpack(call.data)

    if(previous_sent_message[call.message.chat.id] > 0):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=previous_sent_message[call.message.chat.id])

    if(d.previous_answer > 0):
        #check for right answer and update table
        if(getQuizQuestion(d.current_test_id, d.current_question - 1)[1] == d.previous_answer):
            updateToRightAnswer(d.current_test_id, d.current_question - 1)

    if(d.current_question < 10):
        question = getQuizQuestion(d.current_test_id, d.current_question)
        d.current_question+=1
        send_message = await call.message.answer(question[2], reply_markup=getQuizKeyboard(d=d, q = question))
        previous_sent_message[call.message.chat.id] = send_message.message_id

    await call.answer()

