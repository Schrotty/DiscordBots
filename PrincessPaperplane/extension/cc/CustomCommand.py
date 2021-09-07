import os

import yaml
from discord import Message
from discord.ext import commands
from discord.ext.commands import Cog, Bot
from pony.orm import db_session

from extension.cc.models import CustomCommandModel


class CustomCommand(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        # load commands on startup
        self.load_customs()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not message.author.id == self.bot.user.id:
            with db_session:
                command = CustomCommandModel.get(command=message.content)

                if command is not None:
                    command.counter += 1

                    await message.channel.send(command.emit.format(author=message.author.display_name, counter=command.counter))

    @staticmethod
    def load_customs():
        # __file__ or getcwd()?!
        with open("./PrincessPaperplane/extension/cc/commands.yaml", "r") as fs:
            data = yaml.safe_load(fs)

            with db_session:
                for command in data.keys():
                    c = f"{os.getenv('PAPERBOT.BOT.PREFIX')}{command}"

                    if not CustomCommandModel.exists(command=c):
                        CustomCommandModel(command=c, emit=data[command]['emit'], counter=0)
