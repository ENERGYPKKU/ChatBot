from aiogram import types
import random
import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from keyboards import rps_buttons, hello_inline, rps_keyboard, home_keyboard, info_keyboard
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from sqlalchemy import select
from db.models import Base, PlayerScore

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


async def handlers():
    @dp.message_handler(commands=['start'])
    async def say_hello(message: types.Message):
        db_session = message.bot.get("db")

        async with db_session() as session:
            await session.merge(PlayerScore(user_id=message.from_user.id,
                                            score=0,
                                            user_name=message.from_user.username))
            await session.commit()

        await message.answer(
            """Привет 👋🏻, меня зовут (имя), я - телеграм бот 🤖 колледжа ГАПОУ МО ПК "Энергия" СП ЦСП "Энергия, создан для помощи абитуриентам, родителям и студентам. Внизу появились кнопки навигации для начала моей работы 👇🏻""",
            reply_markup=home_keyboard)

    @dp.message_handler(text=['Информация 🤓'])
    async def information_show(message: types.Message):
        await message.answer("О чем мне рассказать? 🤗", reply_markup=info_keyboard)

    @dp.message_handler(text=['Аккаунт 🫵'])
    async def account_show(message: types.Message):
        await message.answer("О чем мне рассказать? 🤗", reply_markup=info_keyboard)

    @dp.message_handler(text=['Задать вопрос ❓'])
    async def question_show(message: types.Message):
        await message.answer("О чем мне рассказать? 🤗", reply_markup=info_keyboard)

    @dp.message_handler(text=['Позвонить 🤳🏻'])
    async def call_show(message: types.Message):
        await message.answer("О чем мне рассказать? 🤗", reply_markup=info_keyboard)

    @dp.message_handler(text=['Специальности 🌐'])
    async def speliazations_show(message: types.Message):
        await message.answer("О чем мне рассказать? 🤗", reply_markup=info_keyboard)

    @dp.message_handler(text=['Форма 🧥'])
    async def form_show(message: types.Message):
        await message.answer("О чем мне рассказать? 🤗", reply_markup=info_keyboard)

    @dp.callback_query_handler(text="stats")
    async def stats(call: types.CallbackQuery):
        await call.answer(cache_time=4)
        db_session = call.bot.get("db")

        async with db_session() as session:
            player: PlayerScore = await session.get(PlayerScore, call.from_user.id)
            score = player.score
        await call.message.answer(f"Your score: {score}")

        db_session = call.bot.get("db")
        sql = select(PlayerScore).order_by(PlayerScore.score.desc()).limit(5)
        text_template = "Top 5 players:\n\n{scores}"
        async with db_session() as session:
            top_players_request = await session.execute(sql)
            players = top_players_request.scalars()

        places = ['🥇', '🥈', '🥉']
        score_entries = [
            f"""{places[index] if len(places)>=index+1 else ""}{index+1}. @{item.user_name}: <b>{item.score}</b>"""
            for index, item in enumerate(players)]
        score_entries_text = "\n".join(score_entries)\
            .replace(f"{call.from_user.id}", f"{call.from_user.id} (it's you!)")
        await call.message.answer(text_template.format(scores=score_entries_text))

    @dp.callback_query_handler(text="play")
    async def stats2(call: types.CallbackQuery):
        await call.answer(cache_time=4)
        await call.message.answer("Rock, paper, scissors...", reply_markup=rps_keyboard)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
