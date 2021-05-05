from pony.orm import PrimaryKey, Required

from core import database


class EmoteRoleSettings(database.Entity):
    _table_ = "emote_role_setting"
    role_id = PrimaryKey(str)
    emote = Required(str)
    text = Required(str)
    min_level = Required(int, sql_default="-1")