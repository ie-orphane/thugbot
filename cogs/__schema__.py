import discord
import traceback
from discord.ext import commands
from datetime import timedelta, datetime, UTC
from utils import clr


class Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def format_timedelta(self, delta: timedelta) -> str:
        """Formats a timedelta duration to [N days] %H:%M:%S format"""
        seconds = delta.seconds

        days, seconds = divmod(seconds, 86_400)
        hours, seconds = divmod(seconds, 3_600)
        minutes, seconds = divmod(seconds, 60)

        days = f"{days} day{'s' if days > 1 else ''} " if days > 0 else ""
        hours = f"{hours:02d}:" if hours > 0 else ""
        minutes = f"{minutes:02d}:" if minutes > 0 else ""

        return f"{days}{hours}{minutes}{seconds:02d}.{delta.microseconds}"

    async def error(self, exception: Exception):
        trace_back = list(traceback.extract_tb(exception.__traceback__)[0])
        await self.bot.get_channel(1233741067048714261).send(
            content=f"```{trace_back[0]}\n  {exception.__traceback__.tb_lineno}\t{trace_back[-1]}\n{exception.__class__.__name__}: {exception}```"
        )

    def start(self, time: datetime, interaction: discord.Interaction):
        print(
            f"{clr.black(time.strftime("%Y-%m-%d %H:%M:%S"))} {clr.green("Cog")}     ",
            f"{clr.magenta(self.qualified_name)} used from {interaction.user} {interaction.guild}"
        )

    async def done(self, interaction: discord.Interaction, Time: datetime):
        if interaction.user.id != 89607124651986945:
            end_time = datetime.now(UTC) - Time
            formated_end_time = self.format_timedelta(datetime.now(UTC) - Time)

            with open("./data/interactions.csv", "a") as file:
                file.write(
                    f"\n{Time},{interaction.user.id},{self.qualified_name},{end_time.total_seconds()}"
                )

            # await self.bot.get_channel(1233741040108961833).send(
            #     embed=discord.Embed(
            #         color=discord.Color.green(),
            #         description=(
            #             f"<t:{int(Time.timestamp())}:F> | **{formated_end_time}**"
            #             f"\n{interaction.channel} | {interaction.guild}"
            #         ),
            #     )
            #     .set_author(name=interaction.user, icon_url=interaction.user.avatar)
            #     .set_footer(text=interaction.user.id)
            # )

            print(
                f"{clr.black(datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"))} {clr.green("Cog")}     ",
                f"{clr.magenta(self.qualified_name)} {interaction.user} done in {formated_end_time}"
            )
