import os
import time
from random import randint

from discord import Member, TextChannel, Guild, Message, Embed
from discord.ext import commands
from discord.ext.commands import Cog
from pony.orm import db_session, select, desc

from core.database import Database
from core.models.models import BannedChannel, UserInfo, LevelReward
from core.rank.experience import *
from core.rank.templates import Template
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
        level_channel: TextChannel = self.bot.get_channel(
            id=int(os.getenv("PAPERBOT.DISCORD.LEVEL_CHANNEL"))
        )

        if message.content == "" or len(message.content) == 0:
            return
        if author.id in self.ignored_user:
            return
        if author.id == self.bot.user.id:
            return

        with db_session:

            # check for banned channels to handle XP and level up
            if not BannedChannel.select(lambda c: c.channel == channel.id).exists():
                user_info: UserInfo = UserInfo.select(
                    lambda u: u.id == author.id
                ).first()

                if user_info is None:
                    user_info = UserInfo(
                        id=str(author.id),
                        name=author.name,
                        exp=0,
                        level=0,
                        exp_time=0,
                        avatar_url=str(author.avatar_url),
                    )

                # has cooldown (60s) expired?
                if (user_info.exp_time + COOLDOWN <= time.time()) or os.getenv(
                    "PAPERBOT.ENVIRONMENT"
                ) == "develop":
                    user_info.exp_time = int(time.time())
                    user_info.exp = user_info.exp + self.calc_xp_reward()

                    level_up = self.get_level_up_threshold(user_info.level)
                    Database.log(
                        Template.GAINED_EP_LOG_MSG.format(
                            GAINED=level_up, CURRENT=user_info.exp
                        )
                    )

                    # missing reward-role check
                    role_high: LevelReward = (
                        LevelReward.select(lambda r: r.reward_level <= user_info.level)
                        .order_by(lambda r: desc(r.reward_level))
                        .first()
                    )
                    role_low: LevelReward = (
                        LevelReward.select(lambda r: r.reward_level <= user_info.level)
                        .order_by(lambda r: r.reward_level)
                        .first()
                    )

                    if role_high is not None and role_low is not None:
                        if role_low not in author.roles:
                            await author.add_roles(
                                guild.get_role(role_id=int(role_low.reward_role))
                            )

                        if role_high not in author.roles:
                            await author.add_roles(
                                guild.get_role(role_id=int(role_high.reward_role))
                            )

                    # trigger level_up if enough XP gained
                    if user_info.exp >= level_up:
                        user_info.level = user_info.level + 1
                        level_reward: LevelReward = LevelReward.select(
                            lambda r: r.reward_level == user_info.level
                        ).first()

                        if level_reward is not None:
                            role_id = int(level_reward.reward_role)
                            role = guild.get_role(role_id=role_id)

                            # give user new role as reward
                            if role not in author.roles:
                                Database.log(
                                    Template.NEW_ROLE_LOG_MSG.format(
                                        AUTHOR=author.name, ROLE=role.name
                                    )
                                )
                                await author.add_roles(role)

                            # remove old reward-roles
                            await level_channel.send(
                                Template.NEW_ROLE_MENTION.format(
                                    MENTION=author.mention, ROLE=role.name
                                )
                            )

                            # DO NOT SIMPLIFY!
                            old_roles = list(
                                select(r.reward_role for r in LevelReward).where(
                                    lambda r: r.reward_level < user_info.level
                                    and r.reward_level > 1
                                )
                            )

                            old_roles = [
                                guild.get_role(role_id=int(r)) for r in old_roles
                            ]

                            for r in old_roles:
                                if r in author.roles:
                                    Database.log(
                                        Template.REMOVE_ROLE_LOG_MSG.format(
                                            AUTHOR=author.name, ROLE=r.name
                                        )
                                    )
                                    await author.remove_roles(r)

    @staticmethod
    def get_level_up_threshold(current_level: int) -> int:
        if current_level > 0:
            return 5 * (current_level ** 2) + 50 * current_level + 100

        return 100

    def calc_xp_reward(self) -> int:
        return self.base_xp + randint(*self.random_xp_range)

    @commands.command(
        aliases=Template.ALIAS, name=Template.COMMAND_NAME, help=Template.HELP_TEXT
    )
    @Checks.is_channel(int(os.getenv("PAPERBOT.DISCORD.BOT_CHANNEL")))
    async def cmd_rank(self, ctx: commands.Context) -> None:
        """Handles rank command

        Args:
            ctx (commands.Context): [description]
        """
        channel: TextChannel = ctx.channel
        author: Member = ctx.author

        with db_session:
            user_info: UserInfo = UserInfo[str(author.id)]

            if user_info is None:
                user_info = UserInfo(
                    id=str(author.id),
                    name=author.name,
                    exp=0,
                    level=0,
                    exp_time=int(time.time()),
                    avatar_url=str(author.avatar_url),
                )

        embed = self.create_rank_display_embed(author, user_info.level, user_info.exp)
        await channel.send(embed=embed)

    def create_rank_display_embed(self, author: Member, level: int, exp: int) -> Embed:
        # generate image with stats
        url = Template.RANK_IMAGE_GENERATOR_URL.format(
            AUTHOR_ID=author.id, TIME=time.time(), EXT=""
        )

        next_level = level + 1
        next_level_up = self.get_level_up_threshold(level)
        exp_left = next_level_up - exp

        # embed current XP, level and missing XP for next level up
        title = Template.RANK_EMBED_TITLE.format(LEVEL=level)
        description = Template.RANK_EMBED_DESCRIPTION.format(
            EXP=exp, NEXT_LEVEL=next_level, EXP_LEFT=exp_left
        )
        colour = author.top_role.colour

        embed = Embed(title=title, description=description, colour=colour)
        embed.set_author(name=author.name, icon_url=author.avatar_url_as(format="png"))
        embed.set_image(url=url)

        return embed
