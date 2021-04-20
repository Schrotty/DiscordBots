import os
import time
from random import randint

from discord import Member, TextChannel, Guild, Message, Embed
from discord.ext import commands
from discord.ext.commands import Cog

from core.database import Database
from core.rank.experience import *
from core.rank.templates import *
from utility.checks import Checks


class Rank(Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.base_xp = BASE
        self.random_xp_range = RANDOM_RANGE
        self.ignored_user = Database.ignored_user()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        await self.handle_user_message_xp(message)

    async def handle_user_message_xp(self, message: Message) -> None:
        author: Member = message.author
        channel: TextChannel = message.channel
        guild: Guild = message.guild
        level_channel: TextChannel = self.bot.get_channel(id=int(os.getenv('PAPERBOT.DISCORD.LEVEL_CHANNEL')))

        if message.content == "" or len(message.content) == 0: return
        if author.id in self.ignored_user: return
        if author.id == self.bot.user.id: return

        # check for banned channels to handle XP and level up
        result = Database.execute("SELECT * FROM level_banned_channel WHERE channel = %s", (channel.id,))
        if result.rowcount == 0:
            result = Database.execute("SELECT exp, expTime, level FROM user_info WHERE id = %s", (author.id,))

            if result.rowcount > 0:
                result = result.fetchone()
                exp = int(result[0])
                expTime = int(result[1])
                level = int(result[2])

                # has cooldown (60s) expired?
                if expTime + COOLDOWN <= time.time():
                    addedExp = self.calc_xp_reward()
                    exp = exp + addedExp

                    levelUp = self.get_levelup_threshold(level)
                    Database.log("Exp for Level-Up: %d, current XP: %d" % (levelUp, exp))

                    # trigger levelup if enough XP gained
                    if exp >= levelUp:
                        level = level + 1
                        exp = 0

                        result = Database.execute("SELECT rewardRole FROM level_reward WHERE rewardLevel = %s",
                                                  (level,))
                        if result.rowcount > 0:
                            roleId = int(result.fetchone()[0])
                            role = guild.get_role(role_id=roleId)

                            # give user new role as reward
                            if role not in author.roles:
                                Database.log("Assign " + author.name + " new role " + role.name)
                                await author.add_roles(role)

                            # remove old reward-roles
                            await level_channel.send(
                                author.mention + " Du hast eine neue Stufe erreicht und erhältst den neuen Rang " + role.name + "!")
                            result = Database.execute(
                                "SELECT rewardRole FROM level_reward WHERE rewardLevel < %s AND rewardLevel > 1",
                                (level,))

                            rows = result.fetchall()
                            for row in rows:
                                role = guild.get_role(role_id=int(row[0]))
                                if role in author.roles:
                                    Database.log("Remove " + author.name + " old role " + role.name)
                                    await author.remove_roles(role)

                    # update user in database with new XP (+ level)
                    Database.execute(
                        "UPDATE user_info SET name = %s, exp = %s, expTime = %s, level = %s, avatar_url = %s WHERE id = %s",
                        (author.name, exp, time.time(), level, author.avatar_url, author.id,))

            # add user to database if missing
            else:
                self.add_user_to_db(author)

    def add_user_to_db(self, author: Member) -> None:
        exp = self.calc_xp_reward()
        Database.execute("INSERT INTO user_info (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, "
                         "%s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url,))

    @staticmethod
    def get_levelup_threshold(current_level: int) -> int:
        level_up = 100
        if current_level > 0:
            level_up = 5 * (current_level ** 2) + 50 * current_level + 100

        return level_up

    def calc_xp_reward(self) -> int:
        return self.base_xp + randint(*self.random_xp_range)

    @commands.command(aliases=['rank', 'rang', 'level', 'lvl'])
    @Checks.is_channel(760861542735806485)
    # @Checks.is_not_in_list(Database.ignored_user()) TODO: Fix this shit!
    async def cmd_rank(self, ctx: commands.Context) -> None:
        """Handles rank command

        Args:
            ctx (commands.Context): [description]
        """
        channel: TextChannel = ctx.channel
        guild: Guild = ctx.guild
        author: Member = ctx.author

        result = Database.execute("SELECT exp, level, name FROM user_info WHERE id = %s", (author.id,))
        row = result.fetchone()

        if result.rowcount == 0:
            Database.execute(
                "INSERT INTO user_info (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)",
                (author.id, author.name, 0, time.time(), author.avatar_url,))

            result = Database.execute("SELECT exp, level, name FROM user_info WHERE id = %s", (author.id,))
            row = result.fetchone()

        # store current variables
        exp = row[0]
        level = row[1]

        # embed = self.create_rank_display_embed(guild, author, level, exp)
        await channel.send()

    def create_rank_display_embed(self, guild: Guild, author: Member, level: int, exp: int) -> Embed:
        # generate image with stats
        url = RANK_IMAGE_GENERATOR_URL.format(AUTHOR_ID=author.id, TIME=time.time(), EXT="")

        next_level = level + 1
        nextLevelUp = self.get_levelup_threshold(level)
        exp_left = nextLevelUp - exp

        # embed current XP, level and missing XP for next levelup
        title = RANK_EMBED_TITLE.format(LEVEL=level)
        description = RANK_EMBED_DESCRIPTION.format(EXP=exp, NEXT_LEVEL=next_level, EXP_LEFT=exp_left)
        colour = author.top_role.colour

        embed = Embed(title=title, description=description, colour=colour)
        embed.set_author(name=author.name, icon_url=author.avatar_url_as(format="png"))
        embed.set_image(url=url)

        return embed
