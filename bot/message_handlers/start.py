from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from .base import BaseHandler
from ..app import bot
from ..dependence import error
from ..settings import PARSE_MODE


class StartHandler(BaseHandler):
    command = ['start', 'restart']
    callback_data = 'start'
    title = 'Вызов меню'

    @error(title=title)
    async def start_handler(self, message: Message, state: FSMContext):
        """
        Этот обработчик будет вызван, когда пользователь отправит команду `/start`.
        Краткая информация о том, как начать работу с ботом.
        :param message: types.Message
        """
        chat_id = message.chat.id
        if chat_id >= 0:
            return await self.handle(message.chat.id, edit_text=chat_id)
        await bot.send_message(message.chat.id,
                               f"<b>Привет, <i>{message.from_user.username}</i>\n</b>"
                               f"Ваш id группы: <b>{message.chat.id}</b>",
                               parse_mode=PARSE_MODE)

    @staticmethod
    async def run_handler(message, state):
        await StartHandler().start_handler(message, state)
