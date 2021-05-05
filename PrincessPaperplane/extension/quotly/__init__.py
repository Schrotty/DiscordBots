from discord.ext.commands import Bot

from extension.quotly.quotly import Quotly


# extension setup
def setup(bot: Bot):
    bot.add_cog(Quotly(bot))
