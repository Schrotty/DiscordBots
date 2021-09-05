from discord.ext.commands import Bot
from extension.hltb.hltb import HLTB


def setup(bot: Bot):
    bot.add_cog(HLTB(bot))
