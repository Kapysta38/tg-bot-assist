from enum import Enum


class Roles(str, Enum):
    admin = "admin"
    chat = "chat"


class StatusProcess(int, Enum):
    stopped = 0
    running = 1
