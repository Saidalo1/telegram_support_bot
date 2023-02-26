import logging

from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN, OWNER
from functions import edit_message
from models import BannedUsers, session

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Greeting message for users and for
    the owner!

    :param message:
    :return:
    """
    if message.from_user.id != OWNER:
        return await message.answer("Welcome to the support bot! You can post questions/suggestions here.")
    else:
        return await message.answer("Welcome boss. Enjoy using the bot!")


@dp.message_handler(commands=['mute'])
async def mute(message: types.Message):
    """
    This feature mutes these users by
    blacklisting a database that the bot
    owner will flag.

    :param message:
    :return:
    """
    if message.from_user.id == OWNER:
        # get replied message
        replied_message = message.reply_to_message.text

        # get chat id
        chat_id = int(replied_message[replied_message.index('[') + 1:replied_message.index(']')])

        # get name of user
        name_of_user = replied_message.split()[4]

        # check user
        banned_user = session.query(BannedUsers).filter(BannedUsers.telegram_id == chat_id).count()
        if not banned_user:
            chat_id = BannedUsers(telegram_id=chat_id)
            session.add(chat_id)
            session.commit()
            return await message.answer(f"{name_of_user} has been blacklisted")
        return await message.answer(f"{name_of_user} has already been banned")
    return await message.answer('You have no right to this!')


@dp.message_handler(commands=['unmute'])
async def unmute(message: types.Message):
    """
    This function unmutes these users by
    removing the users from the blacklisted
    database that the bot owner will mark.

    :param message:
    :return:
    """
    if message.from_user.id == OWNER:
        # get replied message
        replied_message = message.reply_to_message.text

        # get id who sent replied message
        chat_id = int(replied_message[replied_message.index('[') + 1:replied_message.index(']')])

        # get name of user
        name_of_user = replied_message.split()[4]

        # check user id
        chat_id = session.query(BannedUsers).filter(BannedUsers.telegram_id == chat_id)
        if chat_id.count():
            # if user id in black list
            chat_id.delete()
            session.commit()
            return await message.answer(f"{name_of_user} removed from blacklist")
        # if user id is not in black list
        return await message.answer(f'{name_of_user} is not in blacklist')
    return await message.answer("You have no right to this!")


@dp.message_handler()
async def question_users(message: types.Message):
    """
    This function forwards messages between
    regular users and the bot owner.

    :param message:
    :return:
    """
    # if user is owner
    if message.from_user.id == OWNER:
        # if message is not replied
        if not message.reply_to_message:
            return await message.answer("Your message must be a reply to a forwarded message!")
        # if message is replied
        # get replied message
        replied_message = message.reply_to_message.text
        # get id who sent replied message
        chat_id = replied_message[replied_message.index('[') + 1:replied_message.index(']')]
        return await bot.send_message(chat_id, message.text)

    # if user isn't owner
    user_id = message.from_user.id

    # if user is not in black list
    if not session.query(BannedUsers).filter(BannedUsers.telegram_id == user_id).count():
        # edit message
        edited_message = edit_message(message)
        return await bot.send_message(OWNER, edited_message)
    # if user is in black list
    return await message.answer("You are blacklisted by this bot")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
