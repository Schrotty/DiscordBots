from discord import User
from discord.ext import commands
from discord.ext.commands import Context, Cog

from extension.wool.templates import Templates


class Wool(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=Templates.ALIAS, name=Templates.COMMAND_NAME, help=Templates.HELP_TEXT)
    async def wool(self, ctx: Context, user: User):
        await ctx.channel.send(Templates.RESPONSE.format(mention=user.mention))

    async def cog_command_error(self, ctx: Context, error):
        await ctx.send(str(error))
