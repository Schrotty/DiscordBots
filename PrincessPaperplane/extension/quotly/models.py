import os

from pony.orm.core import PrimaryKey, Required, Database

# create database instance
database: Database = Database()


# define models needed for extension
class Quote(database.Entity):
    _table_ = "quotes"
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    author = Required(str)


# connect to database and generate needed tables
database.bind(provider='mysql', host=os.getenv('PAPERBOT.DATABASE.HOST'), user=os.getenv('PAPERBOT.DATABASE.USER'),
              passwd=os.getenv('PAPERBOT.DATABASE.PASSWD'), db=os.getenv('PAPERBOT.DATABASE.DB'))
database.generate_mapping(create_tables=True)
