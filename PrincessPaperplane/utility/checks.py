from typing import Optional

from discord.ext import commands
from discord.ext.commands import Context

from core.models.permission import Permission


class Checks:

    @staticmethod
    def has_permission_for(permission: str):
        async def predicate(ctx: Context):
            return permission in Permission.get_permissions_for_user(ctx.author)

        return commands.check(predicate)

    @staticmethod
    def is_not_in_list(user_list: list):
        async def predicate(ctx):
            return ctx.message.author.id not in user_list

        return commands.check(predicate)

    @staticmethod
    def is_channel(channel_id: int, check_on_server_id: Optional[int] = -1):
        """Checks if bot can accept commands in channel

        Args:
            channel_id (int): Allowed channel
            check_on_server_id (Optional[int], optional): Server ID on which to check for channel. Defaults to 0.

        Returns:
            [type]: Predicate
        """

        # Define predicate to be checked
        async def predicate(ctx):
            if ctx.guild.id == check_on_server_id and ctx.channel.id != channel_id:  # only allow !rank / !rang in
                # #bod_spam
                return False
            else:
                return True

        # Return as check, use with decorator
        return commands.check(predicate)
