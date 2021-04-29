from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Cog, Bot, Context, CommandError
from pony.orm import select, db_session

from core.admin import Template
from core.models.models import BannedChannel
from core.permission import checks

# permissions
LIST_CHANNELS: str = "admin.banned.LIST_CHANNELS"
BAN_CHANNEL: str = "admin.banned.BAN_CHANNEL"
ALLOW_CHANNEL: str = "admin.banned.ALLOW_CHANNEL"


class AdminCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    @checks.has_permission_for(LIST_CHANNELS)
    async def list_banned_channels(self, ctx: Context):
        with db_session:
            banned_channels = list(BannedChannel.select())
            if len(banned_channels) > 0:
                return await ctx.send(
                    Template.LIST_BANNED_CHANNEL.format(CHANNEL=", ".join([ctx.bot.get_channel(id=i).name for i in banned_channels]))
                )

        await ctx.send(Template.NO_BANNED_CHANNEL)

    @commands.command()
    @checks.has_permission_for(BAN_CHANNEL)
    async def ban_channel(self, ctx: Context, channel: TextChannel):
        with db_session:
            if not select(c for c in BannedChannel if c.channel == str(channel.id)).exists():
                BannedChannel(channel=str(channel.id))
                return await ctx.send(Template.CHANNEL_BANNED.format(CHANNEL=channel.name))

        await ctx.send(Template.CHANNEL_ALREADY_BANNED.format(CHANNEL=channel.name))

    @commands.command()
    @checks.has_permission_for(ALLOW_CHANNEL)
    async def allow_channel(self, ctx: Context, channel: TextChannel):
        with db_session:
            if select(c for c in BannedChannel if c.channel == str(channel.id)).exists():
                BannedChannel.select(lambda c: c.channel == str(channel.id)).delete()
                return await ctx.send(Template.CHANNEL_ALLOWED.format(CHANNEL=channel.name))

        await ctx.send(Template.CHANNEL_ALREADY_ALLOWED.format(CHANNEL=channel.name))

    @ban_channel.error
    @allow_channel.error
    async def ignore_channel_error(self, ctx: Context, error: CommandError):
        await ctx.send(str(error))
