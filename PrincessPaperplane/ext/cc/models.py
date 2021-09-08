import os

from pony.orm.core import Database, PrimaryKey, Required, Optional

# create database instance
database: Database = Database()


# define models needed for extension
class CustomCommandModel(database.Entity):
    _table_ = "custom_commands"
    command = PrimaryKey(str)
    emit = Required(str)
    counter = Optional(int)


# connect to database and generate needed tables
database.bind(
    provider="mysql",
    host=os.getenv("PAPERBOT.DATABASE.HOST"),
    user=os.getenv("PAPERBOT.DATABASE.USER"),
    passwd=os.getenv("PAPERBOT.DATABASE.PASSWD"),
    db=os.getenv("PAPERBOT.DATABASE.DB"),
)
database.generate_mapping(create_tables=True)
