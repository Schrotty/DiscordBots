from discord.ext.commands import Bot

from extension.quotly.quote import Quote
from extension.quotly.quotly import Quotly


def setup(bot: Bot):
    bot.add_cog(Quotly(bot))
