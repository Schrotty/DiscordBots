import random

from discord.ext import commands
from discord.ext.commands import Context, Cog, Bot

from core import database
from extension.quotly.quote import Quote, EMPTY

ROLES_WITH_WRITE_ACCESS = 'Schrotty', 763889848149999627  # Discord Roles
TWITCH_USER_WITH_ACCESS = []  # Twitch Names


class Quotly(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        if not database.exist("quotes"):
            self.setup()

        # self.twitch: Twitch = bot.get_cog(Cogs.TWITCH.value)

        # if self.twitch is not None:
        #     self.twitch.twitch_chat.subscribe(self.twitch_command_mapping)

    @staticmethod
    def setup() -> None:
        database.execute(
            'CREATE TABLE quotes(id int auto_increment primary key, quote text not null, author text not null);'
        )

    @staticmethod
    async def post_quote(ctx: Context, quote: Quote):
        return await ctx.channel.send(f'#{quote.id}: "{quote.text}" - {quote.author}')

    @staticmethod
    def fetch_quote() -> Quote:
        result = database.execute('SELECT id, quote, author FROM quotes')
        if result.rowcount <= 0:
            return EMPTY

        return Quote(random.choice(result.fetchall()))

    @staticmethod
    def store_quote(text: str, author: str) -> Quote:
        database.execute('INSERT INTO quotes (quote, author) VALUES (%s, %s)', (text, author,))
        result = database.execute('SELECT id, quote, author FROM quotes WHERE id = (SELECT MAX(id) FROM quotes)')

        return Quote(result.fetchone())

    # def twitch_command_mapping(self, message: twitch.chat.Message) -> None:
    #     if message.text == '!quote':
    #         q = self.fetch_quote()
    #         message.chat.send(f'/me "{q.text}" -{q.author}')
    #
    #     if message.sender in TWITCH_USER_WITH_ACCESS:
    #         if message.text.startswith('!quote add'):
    #             tmp = message.text.split('!quote add')[1].strip().split(maxsplit=1)
    #
    #             if message.text == '!quote add' or len(tmp) < 2:
    #                 return message.chat.send(f'/me @{message.sender} Missing Parameter!')
    #
    #             q = self.store_quote(tmp[1], tmp[0])
    #             return message.chat.send(f'/me @{message.sender} added a new quote from {q.author}.')
    #
    #         if message.text.startswith('!quote help'):
    #             return message.chat.send(f'/me Usage: !quote add <author> <quote>')

    @commands.group()
    async def quote(self, ctx: Context):
        """
        Handles the quote commands.
        """

        if ctx.invoked_subcommand is None:
            quote: Quote = self.fetch_quote()

            if quote is EMPTY:
                return await ctx.channel.send('Found no quote. Add one with !quote add <author> <quote>')

            await self.post_quote(ctx, quote)

    @quote.command(aliases=['add'], name="quote add", help="Adds a new quote.")
    @commands.check_any(commands.has_any_role(ROLES_WITH_WRITE_ACCESS), commands.is_owner())
    async def add_quote(self, ctx: Context, author: str = None, *, text: str = None):
        if author is None:
            return await ctx.channel.send('Author is missing')

        if text is None:
            return await ctx.channel.send('Quote is missing')

        await self.post_quote(ctx, self.store_quote(text, author))

    @add_quote.error
    async def add_quote_error(self, ctx: Context, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'You are not allowed to use this, {ctx.author.mention}')
