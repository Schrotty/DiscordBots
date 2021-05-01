from discord import Member
from pony.orm import db_session, select, PrimaryKey, Required

from core import database

class EntityPermissionMixin(object):

    @staticmethod
    @db_session
    def get_permissions_for_user(member: Member):
        user_roles = [r.id for r in member.roles]

        return list(
            select(p.permission for p in EntityPermission).where(lambda p: p.value == member.id or p.value in user_roles)
        )


class EntityPermission(database.Entity, EntityPermissionMixin):
    _table_ = "entity_permission"
    id = PrimaryKey(int, auto=True)
    value = Required(str)
    permission = Required("Permission")