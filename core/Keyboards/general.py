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

#from core.DataTypes.dbtypes import BookingSelectionCallback


def getMainMenuKeyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text='Профіль📄', callback_data='show_profile')
    keyboard_builder.button(text='Пройти тест', callback_data='start_test')
    keyboard_builder.button(text='Подивитись історію тестів', callback_data='test_history')
    keyboard_builder.button(text='Додати питання до тесту', callback_data='add_question')
    keyboard_builder.button(text='💰 Підтримати проект 💰', callback_data='donate')
    keyboard_builder.button(text='Підтримка (допомога)💬', callback_data='show_support')
    keyboard_builder.button(text='Відгук📊', callback_data='feedback')

    keyboard_builder.adjust(1,2,1,3)

    return keyboard_builder.as_markup()

def getProfileKeyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text='Змінити значок', callback_data='change_display_badge')
    keyboard_builder.button(text='Оновити ім\'я', callback_data='refresh_name')
    keyboard_builder.button(text='Головне меню', callback_data='main_menu')

    keyboard_builder.adjust(2,1)

    return keyboard_builder.as_markup()

def getBackToMainMenuKeyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text='Головне меню', callback_data='main_menu')

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()

def getStartAddingQues():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text='Додати запитання', callback_data='add')

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()
