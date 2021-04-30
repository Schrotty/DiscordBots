from pony.orm import PrimaryKey, Required

from core import database


class BannedChannel(database.Entity):
    _table_ = "level_banned_channel"
    id = PrimaryKey(int, auto=True)
    channel = Required(str)