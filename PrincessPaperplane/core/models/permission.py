from discord import Member
from pony.orm import db_session, select, PrimaryKey, Required

from core import database


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
