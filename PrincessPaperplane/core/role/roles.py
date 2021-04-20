import os
from typing import List

from discord import Member, Guild, Emoji, TextChannel, Message
from discord.ext import commands

from core import Database
from core.role import ROLES_LEVEL, EMOTE_ROLES, EmoteRoleSettings


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # handle added reactions
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.handle_role_reactions(payload)

    # handle removed reactions
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.handle_role_reactions(payload)

    # update role message and add reactions
    async def update_reaction_msg(self, roleChannel, emote_roles: List[EmoteRoleSettings]):
        channel: TextChannel = self.bot.get_channel(id=roleChannel)
        guild: Guild = channel.guild
        msg: Message = None

        async for message in channel.history(limit=200):
            if message.author == self.bot.user:
                msg = message

        if msg is not None:
            for emote in msg.reactions:
                if emote.me:
                    await msg.remove_reaction(emote.emoji, self.bot.user)
        else:
            msg = await channel.send(
                "Hier stehen bald alle Streamer-Rollen, die ihr euch mit dem jeweiligen Emotes als Reaktion geben und "
                "wieder nehmen könnt. :boomerang:")

        string = "Hier stehen alle Rollen, die ihr euch mit den jeweiligen Emotes als Reaktion geben und wieder " \
                 "nehmen könnt:\n "
        for emote_role in emote_roles:
            role = guild.get_role(role_id=emote_role.role_id)

            string_role = 'Rolle %s, %s' % (role.mention, emote_role.emote)
            await msg.add_reaction(emote_role.emote)

            string = string + "\n" + emote_role.text
            if emote_role.role_id in ROLES_LEVEL:
                string = "%s (mindestens Level %d)" % (string, ROLES_LEVEL.get(emote_role.role_id))

        await msg.edit(content=string)

    # handle role reactions
    async def handle_role_reactions(self, payload):
        if payload.channel_id == os.getenv('PAPERBOT.DISCORD.ROLE_CHANNEL'):
            emoji: Emoji = payload.emoji
            guild: Guild = self.bot.get_guild(id=payload.guild_id)
            user: Member = None
            emote_roles: List[EmoteRoleSettings]
            level = 0
            level_channel: TextChannel

            Database.log("Check guild %s" % guild.name)
            Database.log("Check members")
            for member in guild.members:
                Database.log("Check member %s" % member.name)

                if member.id == payload.user_id:
                    Database.log("User found")
                    user = member
                    break

            if user == self.bot.user:
                return

            if user is None:
                Database.log("User is null (User-ID %d, Guild %s) in handle_role_reactions" % (payload.user_id, guild))
                return

            emote_roles = EMOTE_ROLES
            level_channel = self.bot.get_channel(id=int(os.getenv('PAPERBOT.DISCORD.LEVEL_CHANNEL')))

            result = Database.execute("SELECT level FROM user_info WHERE id = %s", (user.id,))
            if result.rowcount > 0:
                level = result.fetchone()[0]

            chosen_emote_role: EmoteRoleSettings
            emote_role_matches: List[EmoteRoleSettings] = list(
                filter(lambda emote_role: emote_role.emote == emoji.name, emote_roles))  # Get matching emote
            if len(emote_role_matches) <= 0:
                # If not match was found, return
                return Database.log("No emote found")
            else:
                chosen_emote_role = emote_role_matches[0]

            role = guild.get_role(role_id=chosen_emote_role.role_id)
            Database.log("Role %s request from %s (Level %d)" % (role.name, user.name, level))

            role: Roles
            if role in user.roles:
                Database.log("Role " + role.name + " removed from " + user.name)
                await user.remove_roles(role)
            else:
                if chosen_emote_role.role_id in ROLES_LEVEL:
                    if level >= ROLES_LEVEL.get(chosen_emote_role.role_id):
                        Database.log("Role " + role.name + " with min-level " + str(
                            ROLES_LEVEL.get(chosen_emote_role.role_id)) + " assigned to " + user.name)
                        await user.add_roles(role)
                    else:
                        await level_channel.send(
                            user.mention + " Du erfüllst das notwendige Level (" + str(level) + " statt " + str(
                                ROLES_LEVEL.get(
                                    chosen_emote_role.role_id)) + ") für die Rolle " + role.name + " nicht!")
                else:
                    Database.log("Role " + role.name + " assigned to " + user.name)
                    await user.add_roles(role)
