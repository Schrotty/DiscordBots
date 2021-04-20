from discord import User
from discord.ext import commands
from discord.ext.commands import Context, Cog

from core import Database


class Wool(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['wolle', 'wa'])
    async def wool(self, ctx: Context, user: User):
        await ctx.channel.send(f'***Achtung!** {user.mention} will wieder Wolle kaufen!*')

    async def cog_command_error(self, ctx, error):
        Database.log(f'Wool -> "{error}"')
