#!/usr/bin/python3
# coding=utf-8


import os
import traceback

import discord
from discord.ext.commands import Bot

import extension
from core import database
from utility import log


class Paperbot(Bot):
    def __init__(self, command_prefix, **options):
        log.setup()
        # ROLES: Roles = self.get_cog(Cogs.ROLES.value)

        super().__init__(command_prefix, **options)

    def boot(self):
        print("Starting PaperBot")
        if os.getenv("PAPERBOT.DISCORD.API") is None:
            return print("Unable to locate API key!")

        return self.run(os.getenv("PAPERBOT.DISCORD.API"))

    # async def on_message(self, message):
    #     if message.guild.id != guild_config.SERVER:  # TODO: Why?
    #         return

    async def on_ready(self):
        try:
            self.user.name = "PaperBot"

            database.log('Bot started')
            print('------')
            print(f'DB.logged in as {self.user.name}#{self.user.id}')
            print('------')

            print('Connected to')
            for guild in self.guilds:
                print("- " + guild.name)

            await self.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(name='twitch.tv/princesspaperplane',
                                                                 type=discord.ActivityType.watching))

            print('------')
            print('Loading Extensions')
            extension.load_extensions(self)

            print('------')
            # await ROLES.update_reaction_msg(guild_config.ROLE_CHANNEL, roles_config.EMOTE_ROLES)
            # await ROLES.update_reaction_msg(os.getenv("DISCORD.CHANNEL.ROLE.LIVE"), roles_config.EMOTE_ROLES)
        except Exception:
            database.log("Error: " + traceback.format_exc())

    def add_cogs(self):
        pass
        # self.add_cog(Rank(self))
        # self.add_cog(Roles(self))
