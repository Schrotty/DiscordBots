import os
import time

from pony.orm.core import PrimaryKey, Required, Database, Optional

# create database instance
database: Database = Database()


# define models needed for extension
class LogInfo(database.Entity):
    _table_ = "log_info"
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    time = Required(int, default=int(time.time()))


class UserInfo(database.Entity):
    _table_ = "user_info"
    id = PrimaryKey(str)
    name = Required(str)
    avatar_url = Optional(str, sql_default="'https://fireabend.community/img/default.png'")
    exp = Optional(int, sql_default=0)
    level = Optional(int, sql_default=0)
    exp_time = Optional(int, sql_default=0)


class LevelReward(database.Entity):
    _table_ = "level_reward"
    id = PrimaryKey(int, auto=True)
    reward_level = Required(int)
    reward_role = Required(str)


class BannedChannel(database.Entity):
    _table_ = "level_banned_channel"
    id = PrimaryKey(int, auto=True)
    channel = Required(str)


class EmoteRoleSettings(database.Entity):
    _table_ = "emote_role_setting"
    role_id = PrimaryKey(str)
    emote = Required(str)
    text = Required(str)
    min_level = Required(int, sql_default="-1")


# connect to database and generate needed tables
database.bind(
    provider="mysql",
    host=os.getenv("PAPERBOT.DATABASE.HOST"),
    user=os.getenv("PAPERBOT.DATABASE.USER"),
    passwd=os.getenv("PAPERBOT.DATABASE.PASSWD"),
    db=os.getenv("PAPERBOT.DATABASE.DB"),
    charset="utf8mb4",
)

database.generate_mapping(create_tables=True)
