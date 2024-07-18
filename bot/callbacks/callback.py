from ..message_handlers import LIST_HANDLERS
from ..dependence.errors import error


class MainCallback:
    state = '*'
    start_with = "!"

    @staticmethod
    def custom_filters(call):
        return MainCallback.start_with in call.data

    @staticmethod
    @error(title="Обработчик кнопок")
    async def callback(callback_query, state):
        await callback_query.answer()

        key = callback_query.data.replace(MainCallback.start_with, '')

        if '-' in key:
            key, value = key.split('-')
        else:
            value = None

        for handler in LIST_HANDLERS:
            if handler.callback_data == key:
                await handler().run(callback_query, state, value)
                return
