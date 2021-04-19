from discord.ext.commands import Bot
from extension.dice.dice import Dice


def setup(bot: Bot):
    bot.add_cog(Dice(bot))
