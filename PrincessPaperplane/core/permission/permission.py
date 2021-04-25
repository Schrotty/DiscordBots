import os

from discord import Member
from pony.orm import Database, PrimaryKey, Required, db_session, select

# create database instance
database: Database = Database()


# define mixin for additional methods
class PermissionMixin(object):
    @staticmethod
    @db_session
    def get_permissions_for_user(member: Member):
        user_roles = [r.id for r in member.roles]

        return list(
            select(p.permission for p in Permission).where(lambda p: p.value == member.id or p.value in user_roles)
        )


# define models needed for permissions
class Permission(database.Entity, PermissionMixin):
    _table_ = "permissions"
    id = PrimaryKey(int, auto=True)
    value = Required(str)
    permission = Required(str)


# connect to database and generate needed tables
database.bind(
    provider="mysql",
    host=os.getenv("PAPERBOT.DATABASE.HOST"),
    user=os.getenv("PAPERBOT.DATABASE.USER"),
    passwd=os.getenv("PAPERBOT.DATABASE.PASSWD"),
    db=os.getenv("PAPERBOT.DATABASE.DB"),
)
database.generate_mapping(create_tables=True)
