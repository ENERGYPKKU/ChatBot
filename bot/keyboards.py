from aiogram import types

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
