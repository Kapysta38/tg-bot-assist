import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = os.path.join('../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv(find_dotenv('../local_data/.env.dev'))

import asyncio
import aioschedule

from aiogram import executor
from bot.settings import DEBUG
from bot.app import dp

from bot.callbacks import LIST_CALLBACKS, LIST_HANDLERS
from bot.loops import LIST_LOOPS
from bot.utils import get_reg_func
from bot.config import get_logger

log = get_logger()


async def scheduler():
    for loop in LIST_LOOPS:
        loop.start()
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    log.info('Start init handlers')

    for handler in LIST_HANDLERS:
        if handler.command is not None:
            dp.register_message_handler(handler.run_handler, commands=handler.command)
        if handler.state is not None:
            list_func = get_reg_func(handler)
            for func in list_func:
                if isinstance(handler.state, list):
                    state = handler.state
                else:
                    state = getattr(handler.state, func.__name__.replace("reg_", ""))
                dp.register_message_handler(func,
                                            text_startswith=handler.text_startswith,
                                            state=state,
                                            content_types=handler.content_types)
        if handler.text_startswith is not None:
            dp.register_message_handler(handler.run_handler, text_startswith=handler.text_startswith)
    log.info('End init handlers')

    log.info('Start init callbacks')
    for callback in LIST_CALLBACKS:
        dp.register_callback_query_handler(callback.callback, callback.custom_filters, state=callback.state)
    log.info('End init callbacks')

    log.info('Start init loops')
    asyncio.create_task(scheduler())
    log.info('End init loops')


if __name__ == '__main__':
    log.info('Бот запущен!')
    if DEBUG:
        log.warning("DEBUG IS ON!!!")
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
