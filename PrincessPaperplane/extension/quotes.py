import random
from typing import List

from discord.ext import commands
from discord.ext.commands import Bot

from core import database


class Quotes(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(aliases=['quote', 'q'])
    async def cmd_quote(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.get_quote(ctx)

    @cmd_quote.command(aliases=['add', 'a'])
    @commands.has_any_role('Schrotty', 763889848149999627)
    async def add_quote(self, ctx: commands.Context, member: str = None, *, quote=None):
        if member is None:
            return await ctx.channel.send("Author is missing!")

        if quote is None:
            return await ctx.channel.send("Quote is missing!")

        # add new quote
        database.execute("INSERT INTO quotes (quote, author) VALUES (%s, %s)", (quote, member,))

        return await ctx.channel.send(f'{ctx.author.name} added the quote "{quote}" from {member}')

    @staticmethod
    async def get_quote(ctx: commands.Context):
        result = database.execute("SELECT quote, author FROM quotes")

        if result.rowcount <= 0:
            return await ctx.channel.send("No quotes found!")

        qs: List = result.fetchall()
        q = random.choice(qs)

        return await ctx.channel.send('"{TEXT}" - {AUTHOR}'.format(TEXT=q[0], AUTHOR=q[1]))


def setup(bot: Bot):
    bot.add_cog(Quotes(bot))

