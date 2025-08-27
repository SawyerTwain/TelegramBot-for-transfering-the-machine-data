from enum import Enum

class CommandType(Enum):
    status_one = "status_one"
    status_all = "status_all"
    help = "help"
    lang = "language"
    set_lang = "set_language"
    start = "start"
