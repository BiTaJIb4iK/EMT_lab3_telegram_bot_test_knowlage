import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, BotCommandScopeDefault, CallbackQuery, ContentType
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from datetime import datetime

from core.Keyboards.general import getMainMenuKeyboard, getProfileKeyboard, getBackToMainMenuKeyboard
from core.Database.user import addUser, checkValidUser, getUser, isUserAdmin
from core.Database.debug import selectTable
from core.Database.questions import getQuizHistory
from core.States.StatesForms import StateForm
from aiogram.fsm.context import FSMContext



async def commandStartHandler(message: types.Message) -> None:
    msg = f'Вітаю <b>{message.from_user.full_name}</b>!\nЦе бот для перевірки знань.'
    addUser(message.from_user.id, message.from_user.full_name)
    await message.answer(msg, reply_markup=getMainMenuKeyboard())



async def commandStartCallback(call: CallbackQuery, bot: Bot) -> None:
    msg = f'Вітаю <b>{call.from_user.full_name}</b>!\nЦе бот для перевірки знань.'
    addUser(call.from_user.id, call.from_user.full_name)
    await call.message.answer(msg, reply_markup=getMainMenuKeyboard())
    await call.answer()



async def showProfile(call: CallbackQuery, bot: Bot) -> None:
    if checkValidUser(call.from_user.id) is True:
        res = getUser(call.from_user.id)
        msg = f"Профіль\nІм'я : {res[1]}\nДата реєстрації : {res[2]}\nAdmin : {res[3]}\n"

        await call.message.answer(msg, reply_markup=getBackToMainMenuKeyboard())

    else:
        #TODO add message to error database 
        logging.error(f"Error user_id is invalid, can't load profile error ID - INVALID_USER_ID : user_id - {call.from_user.id}, select result : {getUser(call.from_user.id)}")
        await call.message.answer(f"<b>Помилка відображення профілю, скопіюйте це повідомлення та напишіть в підтрику</b> : [user_id is invalid, can't load profile error ID - <b>INVALID_USER_ID</b> ]  {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}", parse_mode = ParseMode.HTML)

    await call.answer()
    



async def showDonate(call: CallbackQuery, bot: Bot) -> None:
    await call.message.answer("""
Проект абсолютно <b>безкоштовний</b> та підтримується виключно розробником. Ваша підтримка дуже важлива для нас! 
Ми вдячні за будь-який внесок. Дякуємо тим, хто вже долучився до розвитку проекту.

Додатково, після підтвердження платежу ви отримаєте доступ до бонусів, таких як підвищення рейтингу, значки, розширений функціонал та можливість участі в турнірах.

Всі можливості будуть обиратися демократично за допомогою голосування.

Реквізити для підтримки:
MonoBank: <code>****</code>
PrivatBank: <code>****</code>

Віталій Б.

Дякуємо за вашу підтримку та внесок у розвиток проекту!
""", reply_markup=getBackToMainMenuKeyboard())
    await call.answer()



async def showSupport(call: CallbackQuery, bot: Bot) -> None:
    await call.message.answer("Ви можете звернутися за допомогою в підтримку : @Support", reply_markup=getBackToMainMenuKeyboard())
    await call.answer()

async def giveFeedback(call: CallbackQuery, bot: Bot) -> None:
    await call.message.answer("Ви можете залишити відгук : @Support", reply_markup=getBackToMainMenuKeyboard())
    await call.answer()

    
async def showHistory(call: CallbackQuery, bot: Bot) -> None:
    await call.message.answer("Історія опитувань : \n")
    msgs = getQuizHistory(call.from_user.id)
    for a in msgs:
        await call.message.answer(a)
    await call.answer()

async def addQuestion(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if(isUserAdmin(call.from_user.id)):
        await state.set_state(StateForm.GET_QUESTION) 
        await call.message.answer("Введіть питання : \n")
    else:
        await call.message.answer("У вас немає прав на редагування бази питань\n")
    await call.answer()