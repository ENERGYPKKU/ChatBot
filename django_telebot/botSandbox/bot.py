import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

API_TOKEN = '6109101100:AAFBpIs1Yc3C9wUJXncvJ7oACkfNZtntoNg'
GROUP_ID = -874740801

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define states


class Question(StatesGroup):
    waiting_for_question = State()

# Define command handlers


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Send a message when the command /start is issued.
    """
    await message.reply("Hi there! Press the button to ask a question.")


@dp.message_handler(Command('cancel'), state='*')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    """
    Allow user to cancel action at any time.
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()

    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())

# Define handler for button press


@dp.message_handler(commands=['ask'])
async def ask(message: types.Message):
    """
    Ask user to provide a question.
    """
    await message.reply("What is your question? Use /cancel to stop the conversation.")

    # Set state
    await Question.waiting_for_question.set()

# Define handler for question message


@dp.message_handler(state=Question.waiting_for_question)
async def process_question(message: types.Message, state: FSMContext):
    """
    Receive question from user and forward it to group.
    """
    async with state.proxy() as data:
        data['question'] = message.text

    # Get group id
    chat_id = int(GROUP_ID)
    print(message)

    # Forward message to group
    await message.forward(chat_id)

    # Notify user
    await message.reply("Your message has been forwarded to the group.")

    # Reset state
    await state.finish()


@dp.message_handler()
async def handle_messages(message: types.Message):
    # Check if the message is a reply to a forwarded message from the bot
    print(message.reply_to_message)
    if message.reply_to_message and message.reply_to_message.forward_from:
        # Print the text of the message
        print(f"User replied to forwarded message: {message.text}")


# Define handler for group replies


@dp.channel_post_handler()
async def forward_reply(message: types.Message):
    """
    Forward any replies from group back to user.
    """
    if message.chat.id != int(GROUP_ID):
        return

    # Forward reply to user who asked the question
    user_message = await bot.forward_message(message.from_user.id, message.chat.id, message.message_id)

    # Notify user
    await bot.send_message(user_message.chat.id, f"New answer from {message.from_user.first_name}:\n\n{message.text}")

# Define handler for stopping conversation


@dp.message_handler(commands=['stop'])
async def stop_conversation(message: types.Message):
    """
    Stop the conversation and remove keyboard.
    """
    # Remove keyboard
    markup = types.ReplyKeyboardRemove()

    # Send message to user
    await message.reply("Conversation stopped. Use /start to start again.", reply_markup=markup)

# Start bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
