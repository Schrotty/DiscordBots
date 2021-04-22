from discord.ext import commands
from discord.ext.commands import Context

from core.permission.permission import Permission


def has_permission_for(permission: str):
    async def predicate(ctx: Context):
        return permission in Permission.get_permissions_for_user(ctx.author)

    return commands.check(predicate)
