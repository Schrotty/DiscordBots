from discord.ext import commands
from discord.ext.commands import Cog, Bot, Context
from pony.orm import db_session

from core.admin import Template
from core.models.permission import Permission
from utility import Checks

# permissions
LIST_PERMISSIONS: str = "permissions.LIST"
GRANT_PERMISSIONS: str = "permissions.GRANT"


class PermissionCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    @commands.check_any(Checks.has_permission_for(LIST_PERMISSIONS))
    async def list_permissions(self, ctx: Context):
        with db_session:
            permissions = list(Permission.select())
            if len(permissions) > 0:
                return await ctx.send(
                    Template.LIST_PERMISSIONS.format(
                        PERMISSIONS=", ".join([p.value for p in permissions]))
                )

    @commands.command()
    @commands.check_any(Checks.has_permission_for(GRANT_PERMISSIONS))
    async def grant(self):
        with db_session:
            pass
