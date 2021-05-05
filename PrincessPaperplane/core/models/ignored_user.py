from pony.orm import PrimaryKey

from core import database


class IgnoredUser(database.Entity):
    _table_ = "ignored_user"
    id = PrimaryKey(str)