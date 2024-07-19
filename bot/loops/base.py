import aioschedule

from ..app import bot


class MyBaseLoop:
    title = None

    def __init__(self):
        self.bot = bot

    async def run(self):
        """
        Метод с основной логикой лупа
        :return:
        """
        pass

    def start(self):
        aioschedule.every(1).second.do(self.run)
