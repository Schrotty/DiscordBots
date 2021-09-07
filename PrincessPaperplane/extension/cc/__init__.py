from discord.ext.commands import Bot

from extension.cc.CustomCommand import CustomCommand


def setup(bot: Bot):
    bot.add_cog(CustomCommand(bot))
