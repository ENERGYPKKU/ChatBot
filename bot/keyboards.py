from aiogram import types

inline_info_btn = types.InlineKeyboardButton(
    text="Информация 🤓", callback_data="info")
inline_account_btn = types.InlineKeyboardButton(
    text="Аккаунт 🫵", callback_data="account")
inline_specializations_btn = types.InlineKeyboardButton(
    text="Специальности 🌐", callback_data="specializations")
inline_clothes_form_btn = types.InlineKeyboardButton(
    text="Форма 🧥", callback_data="clothes_form")
inline_ask_question_btn = types.InlineKeyboardButton(
    text="Задать вопрос ❓", callback_data="ask_question")
inline_contact_specialist_btn = types.InlineKeyboardButton(
    text="Обратиться к специалисту 🖋️", callback_data="contact_specialist")
inline_contact_call_btn = types.InlineKeyboardButton(
    text="Позвонить 🤳🏻", callback_data="contact_call")

home_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)
home_keyboard.add(*["Информация 🤓",
                    "Аккаунт 🫵",
                    "Задать вопрос ❓",
                    "Позвонить 🤳🏻"])

info_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)
info_keyboard.add(*["Специальности 🌐", "Форма 🧥"])

inline_stats_button = types.InlineKeyboardButton(
    text="📃 Stats", callback_data='stats')
inline_play_button = types.InlineKeyboardButton(
    text="🎮 Play", callback_data='play')
hello_inline = types.InlineKeyboardMarkup(row_width=2).add(
    inline_stats_button, inline_play_button)

rps_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)
rps_buttons = ['🪨 rock', "📄 paper", "✂ scissors"]
rps_keyboard.add(*rps_buttons)
