from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

inline_info_btn = InlineKeyboardButton(
    text="Информация 🤓", callback_data="info")
inline_account_btn = InlineKeyboardButton(
    text="Аккаунт 🫵", callback_data="account")
inline_specializations_btn = InlineKeyboardButton(
    text="Специальности 🌐", callback_data="specializations")
inline_clothes_form_btn = InlineKeyboardButton(
    text="Форма 🧥", callback_data="clothes_form")
inline_ask_question_btn = InlineKeyboardButton(
    text="Задать вопрос ❓", callback_data="ask_question")
inline_contact_specialist_btn = InlineKeyboardButton(
    text="Обратиться к специалисту 🖋️", callback_data="contact_specialist")
inline_contact_call_btn = InlineKeyboardButton(
    text="Позвонить 🤳🏻", callback_data="contact_call")

home_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)
home_keyboard.add(*[
    "Информация 🤓",
    "Задать вопрос ❓",
    "Контакты 🗒️"])

info_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False, row_width=2)
info_keyboard.add(*["Специальности 🌐", "Форма 🧥", "Назад ↩️"])


inline_phone_keyboard = InlineKeyboardMarkup()


inline_stats_button = InlineKeyboardButton(
    text="📃 Stats", callback_data='stats')
inline_play_button = InlineKeyboardButton(
    text="🎮 Play", callback_data='play')
hello_inline = InlineKeyboardMarkup(row_width=2).add(
    inline_stats_button, inline_play_button)

rps_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)
rps_buttons = ['🪨 rock', "📄 paper", "✂ scissors"]
rps_keyboard.add(*rps_buttons)

inline_form_markup = InlineKeyboardMarkup(row_width=2)

markup = InlineKeyboardMarkup()
markup_search = InlineKeyboardMarkup()
markup_visibility = InlineKeyboardMarkup()

inline_btn_ok = InlineKeyboardButton(
    "✅ Выбрать пользователя", callback_data="user_selected"
)
inline_btn_next = InlineKeyboardButton(
    "❌ Другой пользователь", callback_data="next_user"
)

markup_search.add(inline_btn_next, inline_btn_ok)


inline_btn_vis = InlineKeyboardButton(
    "Доступен для поиска", callback_data="visible")
inline_btn_invis = InlineKeyboardButton("Скрыт", callback_data="invisible")

markup_visibility.add(inline_btn_vis, inline_btn_invis)
