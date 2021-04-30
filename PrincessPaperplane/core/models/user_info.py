from pony.orm import PrimaryKey, Required, Optional

from core import database


class UserInfo(database.Entity):
    _table_ = "user_info"
    id = PrimaryKey(str)
    name = Required(str)
    avatar_url = Optional(str, sql_default="'https://fireabend.community/img/default.png'")
    exp = Optional(int, sql_default=0)
    level = Optional(int, sql_default=0)
    exp_time = Optional(int, sql_default=0)