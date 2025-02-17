#!/usr/bin/python3
# coding=utf-8
import logging
import os

import discord
from discord import Message, ChannelType
from discord.ext.commands import Bot
from pony.orm import db_session

import extension
from core import database
from core.admin.banned_channel_commands import BannedChannelCommands
from core.models.permission import Permission
from core.rank.rank import Rank
from core.role.roles import Roles
from utility.terminal import Terminal


class Paperbot(Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

        # generate database mappings
        database.generate_mapping(create_tables=True)

        self.logger = logging.getLogger("paperbot")

        # register admin commands
        self.add_cog(BannedChannelCommands(self))
        # self.add_cog(PermissionCommands(self))

        # register rand and roles
        self.add_cog(Rank(self))
        self.add_cog(Roles(self))

    def boot(self):
        Terminal.print("Starting PaperBot...")
        if os.getenv("PAPERBOT.DISCORD.API") is None:
            return Terminal.print("Unable to locate API key!")

        with db_session:
            if not Permission.exists():
                # store default roles
                pass

        return self.run(os.getenv("PAPERBOT.DISCORD.API"))

    async def on_message(self, message: Message):
        if message.channel.type in [ChannelType.private, ChannelType.group]:
            return

        await self.process_commands(message)

    async def on_ready(self):
        self.user.name = "PaperBot"

        self.logger.debug("Bot started")
        Terminal.print(f"Logged in as {self.user.name}#{self.user.id}")
        Terminal.empty()

        Terminal.print("Loaded configuration follows:")

        Terminal.print(f'- LEVEL_CHANNEL -> {self.get_channel(id=int(os.getenv("PAPERBOT.DISCORD.LEVEL_CHANNEL")))}')
        Terminal.print(f'- BOT_CHANNEL   -> {self.get_channel(id=int(os.getenv("PAPERBOT.DISCORD.BOT_CHANNEL")))}')
        Terminal.print(f'- ROLE_CHANNEL  -> {self.get_channel(id=int(os.getenv("PAPERBOT.DISCORD.ROLE_CHANNEL")))}')
        Terminal.empty()

        Terminal.print("Connected to")
        for guild in self.guilds:
            Terminal.print(f"- {guild.name}")

        Terminal.empty()

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(name="twitch.tv/princesspaperplane", type=discord.ActivityType.watching),
        )

        Terminal.print("Loading Extensions:")
        extension.load_extensions(self)

        Terminal.empty()
        # await ROLES.update_reaction_msg(guild_config.ROLE_CHANNEL, roles_config.EMOTE_ROLES)
        # await ROLES.update_reaction_msg(os.getenv("DISCORD.CHANNEL.ROLE.LIVE"), roles_config.EMOTE_ROLES)

        Terminal.print("PaperBot started!")
