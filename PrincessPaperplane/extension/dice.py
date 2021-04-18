import os
import re
from random import randint

from discord.ext.commands import Bot, Cog
from discord.ext import commands


class Dice(Cog):
    def __init__(self, bot: Bot):
        prefixes_regex = '(' + "|".join(os.getenv('PAPERBOT.BOT.PREFIX')) + ')'
        self.DICE_CMD_REGEX = re.compile(r"^({prefix})([w,d]\d)".format(prefix=prefixes_regex))
        self.bot = bot
        self.bot.add_listener(self.on_message)

    async def on_message(self, message):
        match = self.DICE_CMD_REGEX.match(message.content)
        if bool(match):
            # Split message content: !w6x8 becomes !w 6x8. Important for command extension, so it can extract parameters
            cmd_length = len(match.group(1)) + len(match.group(2))
            message.content = message.content[:cmd_length] + " " + message.content[cmd_length:]

            await self.bot.process_commands(message)

    @commands.command(aliases=['dice', 'w', 'd'])
    async def cmd_dice(self, ctx: commands.Context, args):
        author = ctx.author

        if 'x' in args:
            dice = int(args.split('x')[0])
            amount = int(args.split('x')[1])
        else:
            dice = int(args)
            amount = 1

        if dice < 1 or amount < 1:
            return

        # print rolled dices
        content = "{MENTION} Du hast folgende Zahlen gewürfelt: ".format(
            MENTION=author.mention)  # Leave whitespace at end!

        for i in range(0, amount):
            if i != 0:
                content = content + ", "
            content = content + str(randint(1, dice))
        await ctx.channel.send(content=content)


def setup(bot: Bot):
    bot.add_cog(Dice(bot))
