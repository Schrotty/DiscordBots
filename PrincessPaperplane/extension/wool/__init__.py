from discord.ext.commands import Bot

from extension.wool.wool import Wool


def setup(bot: Bot):
    bot.add_cog(Wool(bot))
