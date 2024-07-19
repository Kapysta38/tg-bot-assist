from .base import MyBaseLoop
from ..dependence.errors import error
from ..process_handler import Process


class ProcessStartLoop(MyBaseLoop):
    title = 'Запуск приложений'

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.a = 0

    @error(title=title, send_user=False)
    async def run(self):
        """
        Метод с основной логикой лупа
        :return:
        """
        if self.a == 0:
            process = Process(*self.args)
            await process.start()
            self.a += 1
            await process.monitor()

        #
