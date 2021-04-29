from discord.ext import commands
from discord.ext.commands import Context, Cog, Bot
from pony.orm import db_session

from core.permission.checks import has_permission_for
from extension.quotly.models import Quote
from extension.quotly.templates import Template

# permissions
CREATE_QUOTE: str = "quotly.CREATE_QUOTE"
FETCH_QUOTE: str = "quotly.FETCH_QUOTE"


class Quotly(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def post_quote(ctx: Context, quote: Quote):
        await ctx.channel.send(Template.QUOTE.format(ID=quote.id, QUOTE=quote.text, AUTHOR=quote.author))

    @staticmethod
    @db_session
    def fetch_quote() -> Quote:
        return Quote.select_random(limit=1)[0]

    @staticmethod
    @db_session
    def store_quote(text: str, author: str) -> Quote:
        return Quote(text=text, author=author)

    @commands.group()
    @commands.check_any(has_permission_for(FETCH_QUOTE), commands.is_owner())
    async def quote(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            quote: Quote = self.fetch_quote()

            if quote is None:
                return await ctx.channel.send(Template.NO_QUOTE_FOUND)

            await self.post_quote(ctx, quote)

    @quote.command(aliases=Template.ALIAS, name=Template.COMMAND_NAME, help=Template.HELP_TEXT)
    @commands.check_any(has_permission_for(CREATE_QUOTE), commands.is_owner())
    async def add_quote(self, ctx: Context, author: str = None, *, text: str = None):
        if author is None or text is None:
            return await ctx.channel.send(Template.ELEMENT_IS_MISSING)

        await self.post_quote(ctx, self.store_quote(text, author))

    @add_quote.error
    async def add_quote_error(self, ctx: Context, error):
        if isinstance(error, commands.CheckFailure):
            return await ctx.send(Template.MISSING_PERMISSION.format(MENTION=ctx.author.mention))

        await ctx.send(str(error))
