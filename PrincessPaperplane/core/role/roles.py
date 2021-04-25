import os

from discord import Guild, Emoji, TextChannel, Message
from discord.ext import commands
from pony.orm import select, db_session

from core.models.models import UserInfo, EmoteRoleSettings
from core.role.templates import Template


class Roles(commands.Cog):
    @db_session
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emote_roles = list(EmoteRoleSettings.select())

    @commands.Cog.listener()
    async def on_ready(self):
        # await self.update_reaction_msg(int(os.getenv('PAPERBOT.DISCORD.ROLE_CHANNEL')))
        pass

    # handle added reactions
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.handle_role_reactions(payload)

    # handle removed reactions
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.handle_role_reactions(payload)

    # update role message and add reactions
    async def update_reaction_msg(self, role_channel: int):
        channel: TextChannel = self.bot.get_channel(id=role_channel)
        msg: Message = None

        async for message in channel.history(limit=200):
            if message.author == self.bot.user:
                msg = message

        if msg is not None:
            for emote in msg.reactions:
                if emote.me:
                    await msg.remove_reaction(emote.emoji, self.bot.user)
        else:
            msg = await channel.send(Template.TMP_MESSAGE)

        string = Template.ROLE_MESSAGE
        for emote_role in self.emote_roles:
            await msg.add_reaction(emote_role.emote)

            string = string + "\n" + emote_role.text
            if emote_role.min_level != -1:
                string = "%s (mindestens Level %d)" % (string, emote_role.min_level)

        await msg.edit(content=string)

    # handle role reactions
    async def handle_role_reactions(self, payload):
        if payload.channel_id == int(os.getenv("PAPERBOT.DISCORD.ROLE_CHANNEL")):
            emoji: Emoji = payload.emoji
            guild: Guild = self.bot.get_guild(id=payload.guild_id)

            level = 0
            level_channel: TextChannel = self.bot.get_channel(id=int(os.getenv("PAPERBOT.DISCORD.LEVEL_CHANNEL")))

            # checks all guild members to find the one who reacted or get None
            user = guild.get_member(payload.user_id)

            if user is not None:
                with db_session:
                    query = select(u.level for u in UserInfo).where(lambda u: u.id == user.id)

                    if query.exists():
                        level = query.get()

                # find the reaction emote/ the role
                emote_role = [e for e in self.emote_roles if e.emote == emoji.name]
                if len(emote_role) > 0:
                    emote: EmoteRoleSettings = emote_role[0]
                    role = guild.get_role(role_id=int(emote.role_id))

                    if role in user.roles:
                        return await user.remove_roles(role)

                    if level >= emote.min_level:
                        return await user.add_roles(role)

                    return await level_channel.send(
                        Template.LEVEL_TO_LOW.format(
                            MENTION=user.mention,
                            LEVEL=level,
                            MIN_LEVEL=emote.min_level,
                            ROLE=role.name,
                        )
                    )
