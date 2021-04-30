import time

from pony.orm import PrimaryKey, Required

from core import database


class LogInfo(database.Entity):
    _table_ = "log_info"
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    time = Required(int, default=int(time.time()))
