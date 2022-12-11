import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from models import BannedUsers

load_dotenv('.env')
TOKEN = os.environ.get('TOKEN')
OWNER = os.environ.get('OWNER')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['mute', 'unmute'])
async def mute_unmute(message: types.Message):
    replied_message = message.reply_to_message.text
    chat_id = replied_message[replied_message.index('[') + 1:replied_message.index(']')]
    name_of_user = replied_message.split()[4]
    if message.text.startswith('/mute'):
        if not BannedUsers.get_by_id(chat_id):
            chat_id = BannedUsers(chat_id)
            chat_id.save()
            return await message.answer(f"{name_of_user} has been blacklisted")
        return await message.answer(f"{name_of_user} has already been banned")
    if BannedUsers.get_by_id(chat_id):
        chat_id = BannedUsers(chat_id)
        chat_id.delete()
        return await message.answer(f"{name_of_user} removed from blacklist")
    return await message.answer(f'{name_of_user} is not in blacklist')


@dp.message_handler()
async def question_users(message: types.Message):
    if message.from_user.id == OWNER:
        if not message.reply_to_message:
            return await message.answer("Your message must be a reply to a forwarded message!")
        replied_message = message.reply_to_message.text
        chat_id = replied_message[replied_message.index('[') + 1:replied_message.index(']')]
        return await bot.send_message(chat_id, message.text)
    user_id = BannedUsers(message.from_user.id)
    if not BannedUsers.get_by_id(user_id):
        if message.from_user.username is not None:
            edited_message = f"Message from user [{message.from_user.id}] {message.from_user.username}: " \
                             f"\n \n {message.text}"
        else:
            edited_message = f"Message from user [{message.from_user.id}] {message.from_user.full_name}: " \
                             f"\n \n {message.text}"
        return await bot.send_message(OWNER, edited_message)
    return await message.answer("You are blacklisted by this bot")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
