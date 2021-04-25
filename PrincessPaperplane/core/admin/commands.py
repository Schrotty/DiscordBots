from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Cog, Bot, Context, CommandError

from core import Database
from core.admin import Template


class AdminCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def list_banned_channels(self, ctx: Context):
        result = Database.level_banned_channel()
        if len(result) > 0:
            return await ctx.send(
                Template.LIST_BANNED_CHANNEL.format(
                    CHANNEL=", ".join([ctx.bot.get_channel(id=i).name for i in result])
                )
            )

        await ctx.send(Template.NO_BANNED_CHANNEL)

    @commands.command()
    async def ban_channel(self, ctx: Context, channel: TextChannel):
        if (
            Database.execute(
                "SELECT channel FROM level_banned_channel WHERE channel=%s",
                (channel.id,),
            ).rowcount
            == 0
        ):
            result = Database.execute(
                "INSERT INTO level_banned_channel (channel) VALUES (%s)", (channel.id,)
            )
            if result.rowcount > 0:
                return await ctx.send(
                    Template.CHANNEL_BANNED.format(CHANNEL=channel.name)
                )

        await ctx.send(Template.CHANNEL_ALREADY_BANNED.format(CHANNEL=channel.name))

    @commands.command()
    async def allow_channel(self, ctx: Context, channel: TextChannel):
        if (
            Database.execute(
                "SELECT channel FROM level_banned_channel WHERE channel=%s",
                (channel.id,),
            ).rowcount
            > 0
        ):
            result = Database.execute(
                "DELETE FROM level_banned_channel WHERE channel=%s", (channel.id,)
            )
            if result.rowcount > 0:
                return await ctx.send(
                    Template.CHANNEL_ALLOWED.format(CHANNEL=channel.name)
                )

        await ctx.send(Template.CHANNEL_ALREADY_ALLOWED.format(CHANNEL=channel.name))

    @ban_channel.error
    @allow_channel.error
    async def ignore_channel_error(self, ctx: Context, error: CommandError):
        await ctx.send(str(error))
