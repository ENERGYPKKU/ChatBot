from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from main.models import (
    Button
)


cancel_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, row_width=1, one_time_keyboard=True)


try:
    button_cancel = Button.objects.get(role="Остановить диалог").name
except Button.DoesNotExist:
    button_cancel = "Остановить диалог 🛑"

cancel_keyboard.add(*[button_cancel])

home_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)

try:
    button_info = Button.objects.get(role="Информация").name
except Button.DoesNotExist:
    button_info = "Информация 🤓"

try:
    button_question = Button.objects.get(role="Вопрос").name
except Button.DoesNotExist:
    button_question = "Задать вопрос ❓"

try:
    button_contacts = Button.objects.get(role="Контакты").name
except Button.DoesNotExist:
    button_contacts = "Контакты 🗒️"

home_keyboard.add(*[
    button_info,
    button_question,
    button_contacts
])


try:
    button_specialisations = Button.objects.get(role="Специальности").name
except Button.DoesNotExist:
    button_specialisations = "Специальности 🌐"

try:
    button_form = Button.objects.get(role="Форма").name
except Button.DoesNotExist:
    button_form = "Форма 🧥"

try:
    button_back = Button.objects.get(role="Назад").text
except Button.DoesNotExist:
    button_back = "Назад ↩️"

info_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False, row_width=2)

info_keyboard.add(*[
    button_specialisations,
    button_form,
    button_back
])

inline_form_markup = InlineKeyboardMarkup(row_width=2)
inline_spec_markup = InlineKeyboardMarkup(row_width=2)
