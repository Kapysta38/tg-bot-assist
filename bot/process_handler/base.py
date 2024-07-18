import subprocess
import time
import os

from ..api import APIClient
from ..config import logger


class Process:
    def __init__(self, app_command, log_file_path, timeout=60):
        self.app_command = app_command
        slitted_str = log_file_path.split('/')
        self.dir, self.filename = '/'.join(slitted_str[:-1]), slitted_str[-1]
        self.prefix = self.filename.replace(".log", "")
        self.timeout = timeout

        self.process: subprocess.Popen
        self.id: int

    def _register_process(self, pid):
        api = APIClient()
        process = api.create_process(pid=pid, command=self.app_command, log_filename=self.filename)
        self.id = process['id']

    def _start_process(self):
        self.process = subprocess.Popen(self.app_command, shell=True)
        logger.info(f"App {self.process.pid} started.")
        self._register_process(self.process.pid)

    def start(self):
        self._start_process()

    def _restart_process(self):
        self._terminate_process()
        self._start_process()

    def _terminate_process(self):
        api = APIClient()
        api.delete_process(self.id)
        self.process.terminate()
        try:
            self.process.wait(timeout=10)  # Ждем завершения процесса
        except subprocess.TimeoutExpired:
            self.process.kill()  # Принудительно завершаем, если не завершился
        logger.info(f"Process {self.process.pid} has been terminated.")

    def __get_current_log_size(self):
        files = [f for f in os.listdir(self.dir) if f.startswith(self.filename.replace(".log", ''))]
        if not files:
            return None
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.dir, f)))
        return os.path.getsize(os.path.join(self.dir, latest_file))

    def __get_rotation_files_count(self):
        files = [f for f in os.listdir(self.dir) if f.startswith(self.prefix) and f != self.prefix]
        return len(files)

    def monitor(self):
        try:
            last_log_size = self.__get_current_log_size()
            last_rotation_count = self.__get_rotation_files_count()
            while True:
                time.sleep(self.timeout)
                current_log_size = self.__get_current_log_size()
                current_rotation_count = self.__get_rotation_files_count()

                if current_log_size == last_log_size and current_rotation_count == last_rotation_count:
                    logger.info(f"App {self.app_command} has stopped logging. Restarting...")
                    self._restart_process()
                    last_log_size = self.__get_current_log_size()
                    last_rotation_count = self.__get_rotation_files_count()
                    logger.info(f"App {self.app_command} has been restarted.")
                else:
                    last_log_size = current_log_size
                    last_rotation_count = current_rotation_count
        finally:
            self._terminate_process()
