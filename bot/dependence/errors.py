import functools
import traceback

from ..settings import DEBUG, PARSE_MODE
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from ..app import bot
from ..menu import Menu
from aiogram.types import Message, CallbackQuery

from ..api import APIClient
from ..utils import get_users_in_chat_role
from ..config import logger as log


async def send_error(tg_id, ex, tb, title):
    """
    Функция для отправления сообщения об ошибках в админский чат
    :param tg_id: ID пользователя, у которого произошла ошибка.
    :param ex: Ошибка.
    :param tb: Трассировка.
    :param title:
    :return:
    """
    client = APIClient()
    if not DEBUG:
        admin_chat = await get_users_in_chat_role(client)
        if admin_chat:
            admin_chat = admin_chat[0]
        username = await client.get_filter_users(tg_id=tg_id)
        if username:
            username = username[0]['username']
        else:
            username = '-'

        menu = Menu().get_menu('error')
        if tg_id:
            await bot.send_message(admin_chat, menu[0].format(f"{username}", title, ex, tb),
                                   parse_mode=PARSE_MODE)
        else:
            await bot.send_message(admin_chat, menu[0].format("-", title, ex, tb),
                                   parse_mode=PARSE_MODE)
    elif tg_id is not None:
        menu = Menu().get_menu('error')
        await bot.send_message(tg_id, menu[0].format("{username}", title, ex, tb),
                               parse_mode=PARSE_MODE)


def get_msg_and_state(args):
    if len(args) == 1:
        msg = args[0]
        state = None
    elif len(args) == 2:
        msg = args[0]
        state = args[1]
    else:
        msg = args[1]
        state = args[2]
    return msg, state


def get_message_id(msg):
    if isinstance(msg, Message) and not msg.from_user.is_bot:
        message_id = None
    elif isinstance(msg, CallbackQuery):
        message_id = msg.message.message_id
    elif isinstance(msg, Message):
        message_id = msg.message_id
    else:
        message_id = None
    return message_id


def error(title="", send_user=True):
    """
    Декоратор для вывода юзер-френдли сообщения об ошибке для пользователя
    И в чат администраторам
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as ex:
                log.error({'error': ex, 'title': title, 'traceback': traceback.format_exc(120)})
                if send_user and len(args) > 0 and not isinstance(args[-1], bool):
                    msg, state = get_msg_and_state(args)

                    chat_id = msg.from_user.id

                    await send_error(chat_id, ex, traceback.format_exc(120), title)

                    message_id = get_message_id(msg)

                    menu = Menu().get_menu('error', 'user')
                    if message_id is None:
                        await bot.send_message(chat_id, menu[0], reply_markup=menu[1], parse_mode=PARSE_MODE)
                    else:
                        try:
                            await bot.edit_message_text(menu[0], chat_id, message_id, reply_markup=menu[1],
                                                        parse_mode=PARSE_MODE)
                        except MessageNotModified:
                            pass

                    if state and isinstance(state, FSMContext):
                        await state.finish()
                    return
                await send_error(None, ex, traceback.format_exc(120), title)
                return

        return wrapper

    return decorator
