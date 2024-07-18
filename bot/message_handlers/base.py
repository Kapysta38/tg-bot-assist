from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified, BotBlocked

from ..app import bot
from ..menu import Menu
from ..settings import PARSE_MODE
from ..dependence import error


class BaseHandler:
    command = None
    callback_data = None
    state = None
    content_types = None
    text_startswith = None
    title = "Базовые обработчик"

    def __init__(self):
        self.bot = bot
        self.GLOBAL_MENU = Menu()

    async def handle(self, tg_id: int, message_id: int = None, state: bool or str = None, filters: list[str] = None,
                     edit_callback: str or list[str] = None, edit_text: str or list[str] = None,
                     without_kb: bool = False, row: int = None, kb: dict = None):
        text, kb = self.GLOBAL_MENU.get_menu(self.callback_data, state, filters=filters, edit_callback=edit_callback,
                                             row=row, kb=kb)

        if edit_text is not None:
            if isinstance(edit_text, list) or isinstance(edit_text, tuple):
                text = text.format(*edit_text)
            else:
                text = text.format(edit_text)
        if without_kb:
            kb = ReplyKeyboardMarkup()
        try:
            if message_id is None:
                return await self.bot.send_message(tg_id, text[:4096], reply_markup=kb, parse_mode=PARSE_MODE)
            else:
                return await self.bot.edit_message_text(text[:4096], tg_id, message_id, reply_markup=kb,
                                                        parse_mode=PARSE_MODE)
        except BotBlocked:
            return
        except MessageNotModified:
            return

    @error(title=title)
    async def run(self, callback: CallbackQuery, state: FSMContext, data: str = None):
        chat_id, message_id = callback.from_user.id, callback.message.message_id
        template, status = await self.get_template_and_status(callback, state, data=data)
        await self.handle(chat_id, message_id, edit_text=template, state=status)
        await self.set_state(state, chat_id, message_id, data=data)

    async def get_template_and_status(self, callback: CallbackQuery, state: FSMContext, data: str = None):
        """
        Метод создан для переопределения, но не всегда нужен
        :param callback:
        :param state:
        :param data:
        :return:
        """
        return None, None

    async def set_state(self, state: FSMContext, chat_id: int, message_id: int, data: str = None):
        """
        Метод создан для переопределения, но не всегда нужен
        :param state:
        :param chat_id:
        :param message_id:
        :param data:
        :return:
        """
        pass
