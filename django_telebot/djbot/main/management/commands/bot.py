from aiogram.utils import exceptions
from main.models import (
    Form,
    Contact,
    UserMessage,
    BotConfiguration,
    Specialisation
)
from .keyboards import (
    home_keyboard,
    cancel_keyboard,
    info_keyboard,
    inline_form_markup,
    inline_spec_markup,
    button_back,
    button_contacts,
    button_form,
    button_info,
    button_question,
    button_specialisations,
    button_cancel
)

from .messages import (
    hello_msg,
    go_home_msg,
    what_tell_about_msg,
    question_get_msg,
    stop_dialog_msg,
    send_message_to_specialist_msg,
    available_contacts_msg,
    no_contacts_msg,
    available_info_about_form_msg,
    available_info_about_spec_msg,
    user_request_msg,
    specialist_response_msg
)

from aiogram import types as aiogram_types
from aiogram.types import InlineKeyboardButton
from django.db.models import Q
from django.core.management.base import BaseCommand
from django.conf import settings
from channels.db import database_sync_to_async
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
import logging

import json
import os

project_path = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()


class FormState(StatesGroup):
    main_game = State()
    about = State()
    steam_nickname = State()


class FormSearch(StatesGroup):
    choose_game = State()
    choose_player = State()
    user_id = State()


class Question(StatesGroup):
    waiting_for_question = State()


class Command(BaseCommand):
    help = "Telegram Bot"

    def handle(self, *args, **options):
        token = BotConfiguration.objects.filter(
            is_in_use=True).first().bot_token
        bot = Bot(token=token)
        dp = Dispatcher(bot, storage=storage)

        @ database_sync_to_async
        def create_user_message_entity(dict_data):
            UserMessage.objects.create(
                date_timestamp=dict_data["date_timestamp"],
                username=dict_data["username"],
                content=dict_data["content"],
                date=dict_data["date"],
                user_id=dict_data["user_id"]
            )

        @ database_sync_to_async
        def get_chat_id():
            bot_configuration = BotConfiguration.objects.filter(
                is_in_use=True).first()
            return bot_configuration.admin_chat_id

        @ dp.message_handler(commands=["start"])
        async def send_welcome(message: types.Message, state: FSMContext):
            await state.finish()
            await message.answer(hello_msg, reply_markup=home_keyboard
                                 )

        @ dp.message_handler(text=[button_back])
        async def go_back_home(message: types.Message):
            await message.answer(go_home_msg, reply_markup=home_keyboard)

        @ dp.message_handler(text=[button_info])
        async def information_show(message: types.Message):
            await message.answer(what_tell_about_msg, reply_markup=info_keyboard)

        @ dp.message_handler(text=[button_question])
        async def question_set(message: types.Message):

            await message.answer(question_get_msg, reply_markup=cancel_keyboard)

            await Question.waiting_for_question.set()

        @dp.message_handler(Text(equals=button_cancel, ignore_case=True), state='*')
        async def stop_converstation(message: types.Message, state: FSMContext):

            await state.finish()

            await bot.send_message(message.chat.id, stop_dialog_msg, reply_markup=home_keyboard)

        @ dp.message_handler(state=Question.waiting_for_question)
        async def process_question(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data["question"] = message.text
            if (str(message.text).startswith("/")):
                return
            chat_id = int(await get_chat_id())
            dict_data = {
                "date_timestamp": int(message.date.timestamp()),
                "username": message.from_user.username,
                "content": message.text,
                "date": message.date,
                "user_id": message.from_user.id
            }
            await create_user_message_entity(dict_data)
            await message.forward(chat_id)

            await message.reply(send_message_to_specialist_msg, reply_markup=cancel_keyboard)

        @ database_sync_to_async
        def getContactEntitiesMessage():
            if len(Contact.objects.all()) > 0:
                final_array = []
                contacts = Contact.objects.all()
                for contact in contacts:
                    final_array.append(str(contact))
                return available_contacts_msg + "\n" + "\n\n".join(final_array)
            else:
                return no_contacts_msg

        @ dp.message_handler(text=[button_contacts])
        async def call_show(message: types.Message):
            message_text = await getContactEntitiesMessage()
            await message.answer(message_text, reply_markup=home_keyboard)

        @database_sync_to_async
        def get_specialisation_entry_file():
            spec = Specialisation.objects.filter(is_entry=True).first()
            return spec

        @database_sync_to_async
        def get_spec_buttons():
            inline_spec_markup.inline_keyboard = []
            spec_data = Specialisation.objects.all()
            for spec_entity in spec_data:
                spec_entity_inline_btn = InlineKeyboardButton(
                    text=spec_entity.name,
                    callback_data=str(spec_entity.id)
                )
                inline_spec_markup.add(spec_entity_inline_btn)

        @ dp.message_handler(text=[button_specialisations])
        async def speliazations_show(message: types.Message):
            await get_spec_buttons()
            spec = await get_specialisation_entry_file()
            data_path = os.path.join(project_path, 'media/')
            spec_file_path = f"{data_path}{spec.file}"
            with open(spec.file.path, 'rb') as file:
                input_document = types.InputFile(file, spec_file_path)
                await message.answer_document(input_document, caption=available_info_about_spec_msg, reply_markup=inline_spec_markup)

        @database_sync_to_async
        def get_form_entry_file():
            form = Form.objects.filter(is_entry=True).first()
            return form

        @database_sync_to_async
        def get_spec_entity(data):
            spec = Specialisation.objects.get(id=data)
            return spec

        @ dp.message_handler(text=[button_form])
        async def form_show(message: types.Message):
            await getFormButtons()
            form = await get_form_entry_file()
            data_path = os.path.join(project_path, 'media/')
            form_file_path = f"{data_path}{form.file}"
            with open(form.file.path, 'rb') as file:
                input_document = types.InputFile(file, form_file_path)
                await message.answer_document(input_document, caption=available_info_about_form_msg, reply_markup=inline_form_markup)

        @ database_sync_to_async
        def getItemEntity(data):
            try:
                form = Form.objects.get(id=data)
                return ["form", form]
            except Form.DoesNotExist:
                pass
            try:
                spec = Specialisation.objects.get(id=data)
                return ["spec", spec]
            except Specialisation.DoesNotExist:
                pass
            return None

        @ database_sync_to_async
        def getFormButtons():
            inline_form_markup.inline_keyboard = []
            form_data = Form.objects.all()
            for form_entity in form_data:
                form_entity_inline_btn = InlineKeyboardButton(
                    text=form_entity.name,
                    callback_data=str(form_entity.id)
                )
                inline_form_markup.add(form_entity_inline_btn)

        @ dp.callback_query_handler()
        async def inline_callback_handler(query: types.CallbackQuery):
            item_list = await getItemEntity(query.data)
            item = item_list[1]
            message_text = f"{item.name}\n"
            data_path = os.path.join(project_path, 'media/')
            item_file_path = f"{data_path}{item.file}"

            # Good bots should send chat actions...
            await types.ChatActions.upload_document()

            with open(item.file.path, "rb") as file:
                input_file = types.InputFile(
                    filename=item_file_path, path_or_bytesio=file)
                input_document = types.input_media.InputMediaDocument(
                    input_file)
                await query.message.edit_media(input_document)
                if item_list[0] == "form":
                    await query.message.edit_caption(message_text, reply_markup=inline_form_markup)
                if item_list[0] == "spec":
                    await query.message.edit_caption(message_text, reply_markup=inline_spec_markup)

        @ database_sync_to_async
        def get_user_message(date_timestamp):
            try:
                user_message = UserMessage.objects.get(
                    date_timestamp=date_timestamp)
                return user_message.user_id
            except UserMessage.DoesNotExist:
                print("no such message")

        @ database_sync_to_async
        def get_user_message_text(date_timestamp):
            try:
                user_message = UserMessage.objects.get(
                    date_timestamp=date_timestamp)
                return user_message.content
            except UserMessage.DoesNotExist:
                print("no such message")

        @dp.message_handler()
        async def forward_reply(message: types.Message):
            if (str(message.chat.id) != await get_chat_id()):
                return
            if (message["reply_to_message"]):
                try:
                    date_timestamp = int(
                        message.reply_to_message.forward_date.timestamp())
                    chat_id = int(await get_user_message(date_timestamp))
                    user_message_text = await get_user_message_text(date_timestamp)
                    text_message = f"{user_request_msg} \n{user_message_text}\n{specialist_response_msg}\n{message.text}"
                    await bot.send_message(chat_id=chat_id, text=text_message)
                except Exception:
                    print("ошибка отправления")

        executor.start_polling(dp, skip_updates=True)
