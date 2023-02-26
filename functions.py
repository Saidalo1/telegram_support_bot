from aiogram.types import Message


def edit_message(message: Message):
    """
    This function changes the message so that it
    is convenient for the owner of the bot to
    know from which user the message came.

    :param message:
    :return:
    """
    if message.from_user.username is not None:
        edited_message = f"Message from user [{message.from_user.id}] {message.from_user.username}: " \
                         f"\n \n {message.text}"
    else:
        edited_message = f"Message from user [{message.from_user.id}] {message.from_user.full_name}: " \
                         f"\n \n {message.text}"
    return edited_message
