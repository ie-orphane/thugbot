import discord
import traceback
from discord.ext import commands
from models import Emoji
from typing import Optional
from datetime import datetime, UTC, timedelta
from models import HunterData


def format_timedelta(delta: timedelta) -> str:
    """Formats a timedelta duration to [N days] %H:%M:%S format"""
    seconds = delta.seconds

    days, seconds = divmod(seconds, 86_400)
    hours, seconds = divmod(seconds, 3_600)
    minutes, seconds = divmod(seconds, 60)

    days = f"{days} day{'s' if days > 1 else ''} " if days > 0 else ""
    hours = f"{hours:02d}:" if hours > 0 else ""
    minutes = f"{minutes:02d}:" if minutes > 0 else ""

    return f"{days}{hours}{minutes}{seconds:02d}.{delta.microseconds}"


def HunterEmbed(
    member: discord.Member | discord.User,
    highLevel: bool = True,
    level: str | int = "***\u221E***",
    xp: str = "***\u221E***",
    coins: str = "***\u221E***",
    stars: str = "***\u221E***",
):
    return discord.Embed(
        color=discord.Color.dark_blue(),
        description=(
            f"{Emoji.highLevel if highLevel else Emoji.level} Level\u1CBC:\u1CBC{level}\n"
            f"{Emoji.xp} XP{'\u1CBC'*3}:\u1CBC{xp}"
            f"\n{Emoji.star} Stars\u1CBC:\u1CBC{stars}"
            f"\n{Emoji.coin} Coins\u1CBC:\u1CBC{coins}"
        ),
    ).set_author(name=f"{member}", icon_url=member.avatar)


class Hunter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(description="Get information about a Thug Hunter")
    async def hunter(
        self, interaction: discord.Interaction, member: Optional[discord.Member] = None
    ):
        try:
            await interaction.response.defer()
            self.bot.log(
                "Cog", "Balance", f"used from {interaction.user} {interaction.guild}"
            )
            Time = datetime.now(UTC)
            member = member or interaction.user
            if member.id == 1063459223289200652:
                await interaction.followup.send(embed=HunterEmbed(member=member))
            elif error_embed := self.bot.check_hunter(member, interaction):
                await interaction.followup.send(embed=error_embed)
            else:
                hunter = HunterData.read(member.id) or HunterData.create(member.id)

                await interaction.followup.send(
                    embed=HunterEmbed(
                        member=member,
                        highLevel=hunter.level >= 69,
                        level=f"**{hunter.level:n}**",
                        xp=f"**{hunter.xp:n}** / {hunter.required_xp():n}",
                        coins=f"**{hunter.coin:n}**",
                        stars=f"**{hunter.star:n}**",
                    )
                )
        except Exception as e:
            trace_back = list(traceback.extract_tb(e.__traceback__)[0])
            await self.bot.get_channel(1233741067048714261).send(
                content=f"```{trace_back[0]}\n  {e.__traceback__.tb_lineno}\t{trace_back[-1]}\n{e.__class__.__name__}: {e}```"
            )
        else:
            if interaction.user.id != 896071246519869450:
                time = format_timedelta(datetime.now(UTC) - Time)
                hunter.interaction("balance")
                await self.bot.get_channel(1233741040108961833).send(
                    embed=discord.Embed(
                        color=discord.Color.green(),
                        description=(
                            f"<t:{int(Time.timestamp())}:F> | **{time}**"
                            f"\n{interaction.channel} | {interaction.guild}"
                        ),
                    )
                    .set_author(name=interaction.user, icon_url=interaction.user.avatar)
                    .set_footer(text=interaction.user.id)
                )
                self.bot.log(
                    "Cog",
                    "Balance",
                    f"{interaction.user} done in {time}",
                )


#       ranks, userData = rank(id_=member.id), dt(member.id)
#       for name, value in [
#         ("<:rank:1092956484729573450> Rank", f"<:reply:1089853197516029994> Gang: {ranks[1]}\n<:reply:1089853197516029994> Wealth: {ranks[0]}\n<:reply:1089853197516029994> StreetFight: {ranks[2]}\n<:reply:1089853197516029994> VoteStreak: {ranks[3]}")
#       ]:
#         hunterEmbed.add_field(name=name, value=f">>> {value}", inline=name != "<:rank:1092956484729573450> Rank")


async def setup(bot: commands.Bot):
    await bot.add_cog(Hunter(bot))
