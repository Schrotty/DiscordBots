import os
import re
from random import sample, choices
from typing import Optional

from discord.ext import commands
from discord.ext.commands import Bot, Cog

from extension.dice.templates import Templates


class Dice(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.add_listener(self.on_message)

        prefixes_regex = "(" + "|".join(os.getenv("PAPERBOT.BOT.PREFIX")) + ")"
        self.DICE_CMD_REGEX = re.compile(r"^({prefix})([w,d]\d)".format(prefix=prefixes_regex))

    async def on_message(self, message):
        match = self.DICE_CMD_REGEX.match(message.content)
        if bool(match):
            # Split message content: !w6x8 becomes !w 6x8. Important for command extension, so it can extract parameters
            cmd_length = len(match.group(1)) + len(match.group(2))
            message.content = message.content[:cmd_length] + " " + message.content[cmd_length:]

            await self.bot.process_commands(message)

    @commands.command(aliases=Templates.DICE)
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

        # Get dice rolls
        possible_numbers = range(1, dice + 1)
        dice_rolls = choices(possible_numbers, k=amount)

        # print rolled dices
        results = ", ".join(map(str, dice_rolls))
        content = Templates.DICE_RESULT.format(MENTION=author.mention, RESULT=results)

        await ctx.channel.send(content=content)

    @commands.command(aliases=Templates.RANDOM)
    async def random(self, ctx: commands.Context, choice_amount: Optional[int] = 1, *args: str):
        """Wählt zufälliges Element aus

        Args:
            ctx (commands.Context): [description]
        """

        mention: str = ctx.author.mention

        # No values below zero
        if choice_amount <= 0:
            return await ctx.send(Templates.RANDOM_INVALID_NUMER.format(MENTION=mention))

        # Choices have to be given
        if args is None or len(args) <= 0:
            return await ctx.send(Templates.RANDOM_NO_CHOICES.format(MENTION=mention))

        choice_amount = min(choice_amount, len(args))  # Don't go over the amount of possible
        choices = sample(population=args, k=choice_amount)

        await ctx.send(f"{mention}, deine Zufallswahl: {', '.join(map(str, choices))}")
