import time
import os
import psutil

from ..api import APIClient
from ..config import get_logger
from ..app import bot
from ..utils import get_users_in_chat_role

logger = get_logger()


class Process:
    def __init__(self, app_command, log_file_path, timeout=60 * 5):
        self.app_command = app_command
        slitted_str = log_file_path.split('/')
        self.dir, self.filename = '/'.join(slitted_str[:-1]), slitted_str[-1]
        self.prefix = self.filename.replace(".log", "")
        self.timeout = timeout
        self.api = APIClient()
        self.process: psutil.Popen
        self.id: int

    async def _register_process(self, pid):
        process = await self.api.create_process(pid=pid, command=self.app_command, log_filename=self.filename)
        self.id = process['id']

    async def _start_process(self):
        self.process = psutil.Popen(self.app_command, shell=True)
        logger.info(f"App {self.process.pid} started.")
        admin_chat = await get_users_in_chat_role(self.api)
        await bot.send_message(admin_chat[0],
                               f"<b>Приложение {self.app_command.split('/')[-1]} запущено</b>",
                               parse_mode="HTML")
        await self._register_process(self.process.pid)

    async def start(self):
        await self._start_process()

    async def _restart_process(self):
        await self._terminate_process()
        await self._start_process()

    async def _terminate_process(self):
        await self.api.delete_process(self.id)
        try:
            logger.info(f"Terminating process {self.process.pid}...")
            for child in self.process.children(recursive=True):
                logger.info(f"Terminating child process {child.pid}...")
                child.terminate()
            self.process.terminate()
            try:
                self.process.wait(timeout=5)  # Ждем завершения процесса
            except psutil.TimeoutExpired:
                logger.info(f"Killing process {self.process.pid} due to timeout...")
                self.process.kill()  # Принудительно завершаем, если не завершился
            logger.info(f"Process {self.process.pid} has been terminated.")
        except psutil.NoSuchProcess:
            logger.info(f"Process {self.process.pid} already terminated")
        # admin_chat = await get_users_in_chat_role(self.api)
        # await bot.send_message(admin_chat[0],
        #                        f"<b>Приложение {self.app_command.split('/')[-1]} отключено</b>",
        #                        parse_mode="HTML")

    def __get_current_log_size(self):
        files = [f for f in os.listdir(self.dir) if f.startswith(self.filename.replace(".log", ''))]
        if not files:
            return None
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.dir, f)))
        return os.path.getsize(os.path.join(self.dir, latest_file))

    def __get_rotation_files_count(self):
        files = [f for f in os.listdir(self.dir) if f.startswith(self.prefix) and f != self.prefix]
        return len(files)

    async def monitor(self):
        try:
            last_log_size = self.__get_current_log_size()
            last_rotation_count = self.__get_rotation_files_count()
            while True:
                time.sleep(self.timeout)
                current_log_size = self.__get_current_log_size()
                current_rotation_count = self.__get_rotation_files_count()

                if current_log_size == last_log_size and current_rotation_count == last_rotation_count:
                    logger.info(f"App {self.app_command} has stopped logging. Restarting...")
                    admin_chat = await get_users_in_chat_role(self.api)
                    await bot.send_message(admin_chat[0],
                                           f"<b>Приложение {self.app_command.split('/')[-1]} зависло. Перезапуск...</b>",
                                           parse_mode="HTML")

                    await self._restart_process()
                    last_log_size = self.__get_current_log_size()
                    last_rotation_count = self.__get_rotation_files_count()

                    logger.info(f"App {self.app_command} has been restarted.")
                    admin_chat = await get_users_in_chat_role(self.api)
                    await bot.send_message(admin_chat[0],
                                           f"<b>Приложение {self.app_command.split('/')[-1]} перезапущено</b>",
                                           parse_mode="HTML")
                else:
                    last_log_size = current_log_size
                    last_rotation_count = current_rotation_count
        finally:
            await self._terminate_process()
