import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, BotCommandScopeChat, CallbackQuery, ContentType, Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, MagicData, Filter
from aiogram.methods import set_my_commands
from aiogram.methods.set_my_commands import SetMyCommands
from magic_filter import MagicFilter
#from aiogram.types.bot_command_scope_default import BotCommandScopeDefault

import sqlite3

from core.Handlers.main_menu import commandStartHandler, showDonate, showProfile, commandStartCallback, showSupport, giveFeedback, showHistory, addQuestion
from core.Handlers.quiz import start_quiz, answerQuestion
#from core.Middleware.middleware import SelectedCourtMiddleware#, SelectedDayMiddleware, SelectedTimeMiddleware
from core.Database.debug import clearTable, selectTable, printAllTables
from core.Database.basic import setUpDataBaseDefault
from core.Handlers.add_ques import enterQuestion, enterAnswer1, enterAnswer2, enterAnswer3, enterRightAnswer, getRightAnswer
#from core.Database.user import 
from core.States.StatesForms import StateForm
from aiogram.fsm.context import FSMContext

TOKEN = "6753405500:AAF0gpXNEriyZmwf3x5j8MLZ6wqBmfoPUCI"

async def main() -> None:
    #Database section
    #setUpDataBaseDefault()

    #clearTable("Quiz")
    #clearTable("Quiz_questions")
    selectTable("Quiz")
    selectTable("Quiz_questions")
    selectTable("Questions")

    #Bot section
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()

    dp.message.register(commandStartHandler, CommandStart())

    dp.callback_query.register(commandStartCallback, F.data == "main_menu")

    dp.callback_query.register(start_quiz, F.data == "start_test")
    dp.callback_query.register(answerQuestion, F.data.contains("quiz"))
    dp.callback_query.register(showHistory, F.data == "test_history")

    dp.callback_query.register(addQuestion, F.data == "add_question")
    dp.message.register(enterQuestion, StateForm.GET_QUESTION)
    dp.message.register(enterAnswer1, StateForm.GET_ANSWER1)
    dp.message.register(enterAnswer2, StateForm.GET_ANSWER2)
    dp.message.register(enterAnswer3, StateForm.GET_ANSWER3)
    dp.message.register(enterRightAnswer, StateForm.GET_ANSWER4)
    dp.message.register(getRightAnswer, StateForm.GET_RIGHT_ANSWER)

    dp.callback_query.register(showProfile, F.data == "show_profile")
    dp.callback_query.register(showDonate, F.data == "donate")
    dp.callback_query.register(showSupport, F.data == "show_support")
    dp.callback_query.register(giveFeedback, F.data == "feedback")

    await dp.start_polling(bot)

def setUpLoggin():
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the root logger level to the lowest level you want to capture

    # Create a console handler and set the level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  

    # Create a file handler and set the level
    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)  

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Set the formatter for both handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

if __name__ == "__main__":
    setUpLoggin()
    asyncio.run(main())
    #printAllTables()