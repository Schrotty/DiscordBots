from pony.orm import PrimaryKey, Required, Set

from core import database
from core.models.entity_permission import EntityPermission


class Permission(database.Entity):
    _table_ = "permission"
    id = PrimaryKey(int, auto=True)
    value = Required(str)
    entities = Set(EntityPermission)
