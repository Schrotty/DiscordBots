from pony.orm import PrimaryKey, Required

from core import database


class LevelReward(database.Entity):
    _table_ = "level_reward"
    id = PrimaryKey(int, auto=True)
    reward_level = Required(int)
    reward_role = Required(str)