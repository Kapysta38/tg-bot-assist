import json
from pathlib import Path

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..settings import DATA_PATH
from ..config.logging_config import logger as log


class MenuKeyError(Exception):
    pass


class Menu:
    def __init__(self, filename: str = DATA_PATH + "menu.json", encoding='utf-8'):
        filename = Path(filename).resolve()
        self.dict_utils = json.load(open(filename, encoding=encoding))

    def get_item(self, item: str) -> dict:
        try:
            return self.dict_utils[item]
        except KeyError:
            raise MenuKeyError(f'Item {item} does not appear in the list of functions')

    def get_menu(self, item: str, state: bool | str = None, filters: list[str] = None,
                 edit_callback: str | list[str] = None, row: int = None,
                 kb: dict = None) -> tuple[str, InlineKeyboardMarkup]:
        if item not in self.dict_utils.keys():
            raise MenuKeyError(f'Item {item} does not appear in the list of functions')
        state = 'default' if state is None else str(state).lower()
        try:
            result = self.dict_utils[item][state]
            return result['text'], self.get_keyboard(result['utils'] if kb is None else kb, filters=filters,
                                                     edit_callback=edit_callback,
                                                     row=row)
        except KeyError:
            raise MenuKeyError(f"Item {item} has the wrong structure")

    @staticmethod
    def get_keyboard(keyboard: dict, filters: list[str] = None, edit_callback: str | list[str] = None,
                     row_width: int = 2, row: int = None):
        inline_kb = InlineKeyboardMarkup(row_width=row_width)
        row_list = []
        for name, data in keyboard.items():
            callback_data = data['callback_data']

            if edit_callback:
                if isinstance(edit_callback, list):
                    callback_data = callback_data.format(edit_callback.pop(0))
                else:
                    callback_data = callback_data.format(edit_callback)

            if filters and callback_data not in filters:
                continue

            if row is None:
                inline_kb.add(InlineKeyboardButton(name, callback_data=callback_data))
                continue

            if row != len(row_list):
                row_list.append(InlineKeyboardButton(name, callback_data=callback_data))
            elif row == len(row_list):
                inline_kb.row(*row_list)
                row_list = []

        if row and row_list:
            inline_kb.row(*row_list)

        return inline_kb
