from aiogram import types
import random
import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from keyboards import rps_buttons, hello_inline, rps_keyboard
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
            "Hello! Let's play rock, paper, scissors game!",
            reply_markup=hello_inline)

    @dp.message_handler(state="*")
    async def game(message: types.Message):
        if message.text in rps_buttons:
            db_session = message.bot.get("db")
            bot_choice = random.choice(rps_buttons)
            await message.reply(bot_choice)
            win_list = [
                f'{rps_buttons[0]}:{rps_buttons[2]}',  # Rock->Scissors
                f'{rps_buttons[1]}:{rps_buttons[0]}',  # Paper->Rock
                f'{rps_buttons[2]}:{rps_buttons[1]}',  # Scissors->Paper
            ]
            if message.text == bot_choice:
                await message.answer("Tie!")
                return "Tie"
            if f"{message.text}:{bot_choice}" in win_list:
                async with db_session() as session:
                    player: PlayerScore = await session.get(PlayerScore, message.from_user.id)
                    player.score += 1
                    await session.commit()
                await message.answer("You won! +1")
                return "Win"
            if f"{message.text}:{bot_choice}" not in win_list:
                async with db_session() as session:
                    player: PlayerScore = await session.get(PlayerScore, message.from_user.id)
                    player.score -= 1
                    await session.commit()
                await message.answer("You lost! -1")
                return "Los"

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
